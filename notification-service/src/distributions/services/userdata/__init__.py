from typing import Type

from config.settings import FAKE_API
from distributions.services.userdata.api import UserDataAPIClient
from distributions.services.userdata.base import BaseUserDataClient
from distributions.services.userdata.dummy import DummyUserDataClient

UserDataClient: Type[BaseUserDataClient]
if FAKE_API:
    UserDataClient = DummyUserDataClient
else:
    UserDataClient = UserDataAPIClient
