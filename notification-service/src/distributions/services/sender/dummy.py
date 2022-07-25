from distributions.services.sender.base import BaseSender
from distributions.services.userdata.base import UserData


class DummySender(BaseSender):
    def __init__(self, user_data: UserData) -> None:
        super().__init__(user_data)
        self.notification_channel = "dummy"

    def send(self, subject: str, content: str) -> None:
        print(f"Message with subject {subject} sent to {self.user_data.email} {content}")
