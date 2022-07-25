from distributions.services.userdata.base import BaseUserDataClient, UserData


class DummyUserDataClient(BaseUserDataClient):
    def get_user_data(self, user_id) -> UserData:
        return UserData(
            user_id=user_id,
            timezone=0,
            name="veselij",
            email="veselij85@gmail.com",
            mobile="79163377983",
            notification_policy=True,
        )
