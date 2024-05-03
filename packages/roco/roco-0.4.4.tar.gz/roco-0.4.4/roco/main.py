import pathlib
from jinja2 import Environment, PackageLoader, select_autoescape

from .config import get_settings

env = Environment(
    loader=PackageLoader("roco"),
    autoescape=select_autoescape()
)


def get_template():
    cur_dir = pathlib.Path(__file__).parent.resolve()
    template_path = cur_dir / "templates"

    return env.get_template(
        name="runtime-config.js.jinja2",
        parent=str(template_path)
    )


def generate_runtime_config() -> str:
    template = get_template()
    settings = get_settings()

    return template.render(settings)
