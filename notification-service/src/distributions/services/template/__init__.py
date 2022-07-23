from typing import Type

from config.settings import DEBUG
from distributions.services.template.base import BaseTemplate
from distributions.services.template.dummy import DummyTemplate
from distributions.services.template.jinja import JinjaTemplate

Template: Type[BaseTemplate]
if DEBUG:
    Template = DummyTemplate
else:
    Template = JinjaTemplate
