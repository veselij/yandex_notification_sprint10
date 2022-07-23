from distributions.services.sender.base import BaseSender
from distributions.services.userdata.base import UserData


class EmailSender(BaseSender):
    def __init__(self, user_data: UserData) -> None:
        super().__init__(user_data)
        self.notification_channel = "email"

    def send(self, subject: str, content: str) -> None:
        print("Test")
