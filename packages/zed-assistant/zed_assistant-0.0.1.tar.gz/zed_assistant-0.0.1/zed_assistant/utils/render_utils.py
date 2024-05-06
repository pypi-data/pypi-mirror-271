import os
from typing import Dict, Optional

from jinja2 import Template


def render_template(
    origin_path: str,
    template_name: str,
    data: Optional[Dict] = None,
) -> str:
    folder = os.path.dirname(origin_path)
    path = os.path.join(folder, template_name + ".j2")
    with open(path, "r") as file:
        template = Template(file.read())
        return template.render(data or {})
