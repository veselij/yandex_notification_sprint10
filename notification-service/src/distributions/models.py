import uuid

from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Channels(models.TextChoices):

    email = "email", _("email")
    sms = "sms", _("sms")


class TimeStampedMixin(models.Model):
    """Mixin to extend class models with date fields create and modified."""

    name = models.CharField(_("name"), max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NotificationTemplates(TimeStampedMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(_("subject"), max_length=255)
    content = RichTextField(
        _("content"),
        help_text="в шаблоне можно использовать переменные {{name}} - имя и {{content}} - содержание уведомления",
    )
    channel = models.TextField(_("channel"), choices=Channels.choices, max_length=8)

    class Meta:
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")

    def __str__(self) -> str:
        return f"{self.name} {self.channel}"


class AuthUser(models.Model):

    auth_user_id = models.UUIDField(primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)


class NotificaionDistribution(TimeStampedMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = RichTextField(
        _("content"),
    )
    template = models.ForeignKey(
        NotificationTemplates, on_delete=models.CASCADE, verbose_name=_("template")
    )

    class Meta:
        verbose_name = _("NotificaionDistribution")
        verbose_name_plural = _("NotificaionDistributions")

    def __str__(self) -> str:
        return self.name
