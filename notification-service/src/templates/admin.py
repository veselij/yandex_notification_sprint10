from django.contrib import admin
from django.shortcuts import render

from .models import Template
from .forms import NotificationForm


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    actions = ["create_notification"]

    def create_notification(self, request, queryset):

        if "apply" in request.POST:
            print(request.POST)
            print(queryset)
            user_id = request.POST["user_id"]
            periodicity = request.POST["periodicity"]
            notification_text = request.POST["notification_text"]
        else:
            form = NotificationForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
            return render(request,
                          "admin/create_notification.html",
                          context= {'form': form})

    create_notification.short_description = "Create notification"
