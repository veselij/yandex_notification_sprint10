``` mermaid
flowchart 

Kafka[[KAFKA/RABBITMQ]]

subgraph Auth
    AuthNewUser(Auth New user event)
    EndPoint(End Point confirm email)
end

subgraph UGC
    UgcLike(UGC Comment Like event)
end

subgraph Admin Portal
    Admin(Send email event)
    CeleryGui(Celery GUI task manager)
    MailDist(GUI mail preararation)
    DbAdmin[(DB celery tasks \n email tempates)]

    CeleryGui ---> DbAdmin
    MailDist --> DbAdmin
    MailDist --->Admin
end

Db[("Database tables: \n {notification_id, notification_name, user_id, content_id, content_value, template_id}")]
Celery(Celery Periodic tasks \n and related queue and workers)
CeleryQ[[Celery email task queue]]
Worker(Celery Email Worker)

subgraph Consumer
    direction TB
    UserNew("New user consumer create rows: \n {notification_id, notification_name, user_id, content_id, content_value, template_id}")
    UgcConsumer("New comment like consumer create row or update value \n (key = user_id+content_id): \n {notification_id, notification_name, user_id, content_id, content_value, template_id} \n content_value, ++1 if row exists \n template_id - consumer knows")
    MailingConsumer("New mailing distribution create row or update value \n (key = user_id+content_id): \n {notification_id, notification_name, user_id, content_id, content_value, template_id} \n content_value-any text, replaced if row exists \n template_id - consumer knows")

end

UserNew --> Db
UserNew --send notification immediately --> Celery
MailingConsumer --> Db
MailingConsumer --send notification immediately --> Celery
UgcConsumer --> Db
AuthNewUser -- new user registered --> Kafka
UgcLike --new like for comment --> Kafka
Admin --admin made new mailing compain --> Kafka
Kafka --> UserNew
Kafka -->UgcConsumer
Kafka -->MailingConsumer
Db <--Tasks periodically read db events--> Celery
Celery --"if some data ready \n check policy, if ok put to Queue with timezone adjustment  \n {notificaiton_id, email, subject, body}"--> CeleryQ
CeleryQ <-- worker listen for the task --> Worker
Celery --get tasks--> DbAdmin
Celery -- get template --> DbAdmin
Worker --update notification status --> Db
Worker -- fill template with content and send email --> Sangrid((Sangrid))

AuthPersonalData(Internal API in Auth to get user data)
Celery -- get email, name, timezone,\n notification policy --> AuthPersonalData
```

Input Queue (принимает сообщения от других сервисов) format message:
```
{
    "user_id": "uuid,
    "notification_name": "text",
    "content_id": "uuid",
    "content_value": "text"
}
```
в шаблонах jinja можно сделать помимо переменной персональных данных name - переменную content_value куда встраивать content_value из сообщения в брокере
В Celery с помощью django-celery-beat создаем x тасков с параметрами имя нотификейшена, тема письма, число дней между уведомлениями - раз в x, каждый таск запускает свой воркер который делает:
1. Ходит в DB выбирает строки со своим именем. 
2. дальше такс идет в Auth API и берет email, name, timezone, notification policy по user_id
3. проверяет если notification policy allowed (для упрощения используем только один флаг для всех уведомлений true/false - потом расширим) и email верефицирован. Если все ок, то ставит новую таску со смещением по таймзоне. В нашем сервисе работаем только с положительными таймзонами (считаем это нашим регионом):
4. После наступления таска, берем актуальный контент из БД, смотрим не было ли отправлено сообщено другим брокером, если все ок, то 
    - идет в базу за шаблоном  jinja и подставляет туда контент и перснональные данные
    - ставит в очередь заданий celery задание с поправкой по всем каналам 
5. После рассылки обновляем БД и ставим во сколько какой канал отправил сообщение
