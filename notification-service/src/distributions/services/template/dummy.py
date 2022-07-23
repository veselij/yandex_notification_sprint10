from distributions.services.template.base import BaseTemplate


class DummyTemplate(BaseTemplate):
    def get_content(self, content: str, name: str) -> str:
        return f"This is test message to {name} with no body for notification_id {content}"
