from distributions.models import NotificaionDistribution, NotificationTemplates
from django.contrib import admin


@admin.register(NotificationTemplates)
class NotificationTemplatesAdmin(admin.ModelAdmin):

    list_display = ("name", "channel")


@admin.register(NotificaionDistribution)
class NotificaionDistributionAdmin(admin.ModelAdmin):

    list_display = ("name",)
