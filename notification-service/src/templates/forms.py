import enum

from django import forms

periodicity = (
    ("once", "once"),
    ("daily", "daily"),
    ("weekly", "weekly"),
)


class NotificationForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    user_id = forms.CharField(widget=forms.TextInput)
    periodicity = forms.ChoiceField(choices=periodicity)
    notification_text = forms.CharField(widget=forms.Textarea)
