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

Db[("Database tables: \n {notification_id, user_id, message_id, periodicity, last_update, status} \n {message_id, content_id, content_value, template_id}")]
Celery(Celery Periodic tasks \n and related queue and workers)
CeleryQ[[Celery email task queue]]
Worker(Celery Email Worker)

subgraph Consumer
    direction TB
    UserNew("New user consumer create rows: \n {notification_id, user_id, message_id, periodicity, last_update, status} \n {message_id, content_id, content_value, template_id} \n content_id-empty, content_value-link for confirmation \n template_id - consumer knows")
    UgcConsumer("New comment like consumer create row or update value \n (key = user_id+content_id): \n {notification_id, user_id, message_id, periodicity, last_update, status} \n {message_id, content_id, content_value, template_id} \n content_value-1, ++1 if row exists \n template_id - consumer knows")
    MailingConsumer("New mailing distribution create row or update value \n (key = user_id+content_id): \n {notification_id, user_id, message_id, periodicity, last_update, status} \n {message_id, content_id, content_value, template_id} \n content_value-any text, replaced if row exists \n template_id - consumer knows")

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
    "periodicity": "once, daily, weekly",
    "content_id": "uuid",
    "content_value": "text"
}
```
Celery Queue message format (отдельная очередь в том же RabbitMQ):
```
{
    "notification_id": "uiud",
    "email": "email@main.ru",
    "subject": "subject",
    "body": "email body composed from jinja template, variable and content_value"
}
```
в шаблонах jinja можно сделать помимо переменной персональных данных name - переменную content_value куда встраивать content_value из сообщения в брокере
В Celery с помощью django-celery-beat создаем 2 таска - раз в день и раз в неделю, каждый таск запускает свой воркер который делает:
1. Ходит в DB выбирает строки своей периодичности и смотрит поле last_update != текущему периоду и статус не ОК. Т.е. забирает все строки своей периодичности, которые еще не были отработаны или были неуспешно отработаны.
2. дальше такс идет в Auth API и берет email, name, timezone, notification policy по user_id
3. проверяет если notification policy allowed:
    - идет в базу за шаблоном  jinja и подставляет туда контент и перснональные данные
    - ставит в очередь заданий celery отложенное задание с поправкой на таймзону