import jinja2
from distributions.services.template.base import BaseTemplate
from distributions.services.userdata.base import UserData


class JinjaTemplate(BaseTemplate):
    def get_content(self, content: str, userdata: UserData) -> str:
        environment = jinja2.Environment(autoescape=True)
        content_template = environment.from_string(self.template.content)
        return content_template.render(name=userdata.name, content=content)

    def get_subject(self) -> str:
        return self.template.subject
