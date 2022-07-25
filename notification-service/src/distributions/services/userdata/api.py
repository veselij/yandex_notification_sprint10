from json import JSONDecodeError

import requests
from distributions.services.exceptions import NoUserDataExceptionError
from distributions.services.userdata.base import BaseUserDataClient, UserData
from django.conf import settings
from requests.status_codes import codes


class UserDataAPIClient(BaseUserDataClient):
    def get_user_data(self, user_id) -> UserData:
        request = requests.get(
            settings.AUTH_URL.format(settings.AUTH_HOST, settings.AUTH_PORT, user_id),
            timeout=10,
        )
        if request.status_code != codes.ok:
            raise NoUserDataExceptionError("not OK replay from AUTH")
        try:
            user_data = request.json()
        except JSONDecodeError as e:
            raise NoUserDataExceptionError(str(e))

        return UserData(**user_data)
