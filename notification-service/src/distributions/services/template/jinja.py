from distributions.services.template.base import BaseTemplate
from distributions.services.userdata.base import UserData


class JinjaTemplate(BaseTemplate):
    def __init__(self, template_id: str) -> None:
        self._template_id = template_id

    def get_content(self, content: str, userdata: UserData) -> str:
        # TODO load template from db which will be done in separate Task by Nikita
        return f"<p>Jinja Email content loaded from template for user {userdata.name} with content {content}</p>"

    def get_subject(self) -> str:
        # TODO load template from db which will be done in separate Task by Nikita
        return "subject"
