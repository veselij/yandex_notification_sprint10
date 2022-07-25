import sendgrid
from celery.utils.log import get_task_logger
from distributions.services.exceptions import RepeatTaskExceptionError
from distributions.services.sender.base import BaseSender
from distributions.services.userdata.base import UserData
from django.conf import settings
from python_http_client.exceptions import GatewayTimeoutError
from sendgrid.helpers.mail import Content, Email, Mail, To

logger = get_task_logger(__name__)


class SangridSender(BaseSender):
    def __init__(self, user_data: UserData) -> None:
        super().__init__(user_data)
        self.notification_channel = "email"

    def send(self, subject: str, content: str) -> None:
        sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        from_email = Email(settings.EMAIL)
        to_email = To(self.user_data.email)
        email_content = Content("text/html", content)
        mail = Mail(from_email, to_email, subject, email_content)
        mail_json = mail.get()

        try:
            sg.client.mail.send.post(request_body=mail_json)
        except GatewayTimeoutError as e:
            logger.exception(e)
            raise RepeatTaskExceptionError(str(e))
