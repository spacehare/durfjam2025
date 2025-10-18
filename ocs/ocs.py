from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

import yaml
from jinja2 import Template
from markdown2 import markdown
from weasyprint import CSS, HTML

OCS_STEM: str = r"ocs"
PDF_STEM = "bestiary"

OCS_HTML_PATH: Path = Path(f"ocs/{OCS_STEM}.html")
OCS_YAML_PATH: Path = Path(f"ocs/{OCS_STEM}.yaml")

OCS_PDF_PATH: Path = Path(f"out/{PDF_STEM}.pdf")
OCS_CSS_BUILD_PATH: Path = Path(f"out/out.css")


class Pronouns(NamedTuple):
    # https://en.pronouns.page/he
    subject: str
    object: str
    possessive_determiner: str
    possessive_pronoun: str
    reflexive: str

    @staticmethod
    def from_subject(string: str, pronouns: dict) -> 'Pronouns':
        return Pronouns(*pronouns[string])

    def __repr__(self):
        return f"[{', '.join([self.subject, self.object, self.possessive_pronoun])}]"


@dataclass
class NPC:
    name: str
    origin: str
    pronouns: list[Pronouns]
    skill: int | None
    hd: int | None
    armor: int | None
    morale: int | None
    desc: str
    abils: list[str] = field(default_factory=list[str])

    @staticmethod
    def from_dict(d: dict, all_pronouns: dict) -> 'NPC':
        npc = NPC(
            name=d['name'],
            origin=d.get('from', ""),
            pronouns=[
                Pronouns.from_subject(p, all_pronouns) for p in d.get('pronouns', [])
            ],
            hd=d.get('hd', None),
            armor=d.get('armor', None),
            morale=d.get('morale', None),
            skill=d.get('skill', None),
            desc=d.get('desc', ""),
            abils=d.get('abils', []),
        )
        npc.desc = str(markdown(npc.desc))
        npc.abils = [str(markdown(s)) for s in npc.abils]

        for a in d.get('abils', ''):
            if '**Spells**' in a:
                print(a)
                print(markdown(a))

        return npc


def main() -> None:
    html_raw: str = OCS_HTML_PATH.read_text()
    template: Template = Template(html_raw)

    data: dict = yaml.safe_load(OCS_YAML_PATH.open())
    ocs: list[NPC] = [NPC.from_dict(oc, data['pronouns']) for oc in data['ocs']]

    data_dict: dict = {'bestiary': {'ocs': ocs}}
    html_rendered: str = template.render(data_dict)

    css_tailwind: CSS = CSS(string=OCS_CSS_BUILD_PATH.read_text())
    reset = CSS(string=Path("ocs/reset.css").read_text())

    HTML(string=html_rendered).write_pdf(
        OCS_PDF_PATH,
        stylesheets=[reset, css_tailwind],
    )


if __name__ == '__main__':
    main()
