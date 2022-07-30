import uuid

from django.core.exceptions import ValidationError
from jinja2 import Template as JinjaTemplate

from django.db import models
from tidylib import tidy_document


class Template(models.Model):
    id = models.UUIDField("id", primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField("title", max_length=255)
    body = models.TextField("template_body")

    def clean(self) -> None:
        template_body = JinjaTemplate(self.body)
        document, errors = tidy_document(template_body)
        if errors:
            raise ValidationError("Errors in html template body")
        print(template_body.render({}))

    def __str__(self):
        return self.subject
