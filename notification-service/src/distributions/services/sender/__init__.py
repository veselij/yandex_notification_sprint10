from typing import Type

from config.settings import FAKE_EMAIL_PROVIDER
from distributions.services.sender.base import BaseSender
from distributions.services.sender.dummy import DummySender
from distributions.services.sender.email import SangridSender

EmailSender: Type[BaseSender]
if FAKE_EMAIL_PROVIDER:
    EmailSender = DummySender
else:
    EmailSender = SangridSender
