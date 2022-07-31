``` mermaid
flowchart 

Kafka[[RABBITMQ]]

subgraph Auth
    AuthNewUser(Auth New user event producer)
    EndPoint(End Point confirm email)
end

subgraph UGC
    UgcLike(UGC Comment Like event producer)
end

subgraph Admin Portal
    Admin(Send periodic emails)
    AdminOne(Send one-time emails)
    CeleryGui(Celery GUI task manager for \n periodic events)
    MailDist(GUI mail template preparation)
    DbAdmin[(DB celery tasks \n email templates)]
    Celery(Celery Periodic tasks manager)

    CeleryGui ---> DbAdmin
    MailDist --> DbAdmin
    MailDist --->Admin
    MailDist --->AdminOne
end

Db[("Database tables: \n {notification_id, notification_name, user_id, content_id, content_value, template_id, email_last_send}")]
CeleryQ[[Celery notification tasks scheduler with timezones]]
Worker(Celery notification executor)

subgraph Consumer
    direction TB
    UserNew("New user consumer")
    UgcConsumer("New comment like consumer")
    MailingConsumer("New mailing distribution consumer")
end

UserNew --> Db
UserNew --send notification immediately --> CeleryQ
MailingConsumer --> Db
UgcConsumer --> Db
AuthNewUser -- new user registered --> Kafka
UgcLike --new like for comment --> Kafka
AdminOne --admin made one time --> Kafka
AdminOne --admin made one time --> CeleryQ
Admin --admin made new mailing compain --> Kafka
Kafka --> UserNew
Kafka -->UgcConsumer
Kafka -->MailingConsumer
Db <--Tasks periodically read db events--> Celery
Celery --> CeleryQ
CeleryQ <-- worker listen for the task --> Worker
Celery --get tasks--> DbAdmin
Worker --get latest content, check send and update notification status --> Db
Worker -- fill template with content, check that it was not send already and send notification via registered channels --> Sangrid((Notification Channel))

AuthPersonalData(Internal API in Auth to get user data)
CeleryQ -- get email, name, timezone,\n notification policy --> AuthPersonalData
```

Input Queue Rabbit (принимает сообщения от других сервисов) format message:
```
{
    "user_id": "uuid,
    "notification_name": "text",
    "content_id": "uuid",
    "content_value": "text"
    "template_id": "uuid"
}
```
New user flow example

``` mermaid
sequenceDiagram
participant A as Auth
participant R as Rabbit
participant C as Consumer
participant M as Mongo
participant Ce as Celery
participant Ad as Django Admin
participant Ch as Notification Channel

A->>R: Publish new user event
C->>R: Read new user event
C->>C: processed event
C->>M: save new notification data
C->>Ce: triggers task to create new user in django admin
C->>Ce: triggers notification distribution task
Ce->>A: get user data
A-->>Ce: send user data
Ce->>Ce: check that notification allowed and scheduler notification send task according timezone
Ce->>M: get lates notification content and last time when notification was send if was
Ce->>Ad: get template 
Ce->>Ce:fill with content
Ce->>Ch: send notification
Ce->>M: execute task callback to update last sent time
```