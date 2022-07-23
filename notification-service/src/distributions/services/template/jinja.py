from distributions.services.template.base import BaseTemplate


class JinjaTemplate(BaseTemplate):
    def __init__(self, template_id: str) -> None:
        self._template_id = template_id

    def get_content(self, content: str, name: str) -> str:
        # TODO load template from db which will be done in separate Task by Nikita
        return f"Jinja Email content loaded from template for user {name} with content {content}"
