from distributions.models import NotificaionDistribution
from distributions.tasks import create_notifications
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=NotificaionDistribution)
def notification_handler(sender, instance, **kwargs) -> None:
    create_notifications.delay(
        instance.name, "", instance.content, instance.template.name
    )
