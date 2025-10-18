from pathlib import Path

import markdown2
import yaml
from jinja2 import Template
from weasyprint import CSS, HTML

OCS_STEM: str = r"ocs"
PDF_STEM = "bestiary"

OCS_HTML_PATH: Path = Path(f"ocs/{OCS_STEM}.html")
OCS_YAML_PATH: Path = Path(f"ocs/{OCS_STEM}.yaml")

OCS_PDF_PATH: Path = Path(f"out/{PDF_STEM}.pdf")
OCS_CSS_BUILD_PATH: Path = Path(f"out/out.css")


def main() -> None:
    html_raw: str = OCS_HTML_PATH.read_text()
    template: Template = Template(html_raw)

    ocs_data = yaml.safe_load(OCS_YAML_PATH.open())
    data_dict: dict = {'bestiary': ocs_data}

    html_rendered: str = template.render(data_dict)
    css_tailwind: CSS = CSS(string=OCS_CSS_BUILD_PATH.read_text())

    HTML(string=html_rendered).write_pdf(OCS_PDF_PATH, stylesheets=[css_tailwind])


if __name__ == '__main__':
    main()
