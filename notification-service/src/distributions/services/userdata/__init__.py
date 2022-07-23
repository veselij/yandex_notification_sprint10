from typing import Type

from config.settings import DEBUG
from distributions.services.userdata.base import BaseUserDataClient
from distributions.services.userdata.dummy import DummyUserDataClient
from distributions.services.userdata.email import UserDataAPIClient

UserDataClient: Type[BaseUserDataClient]
if DEBUG:
    UserDataClient = DummyUserDataClient
else:
    UserDataClient = UserDataAPIClient
