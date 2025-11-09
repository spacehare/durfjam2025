import argparse
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

import yaml
from jinja2 import Template
from markdown2 import markdown
from weasyprint import CSS, HTML

logger = logging.getLogger('weasyprint')
logger.setLevel(logging.WARNING)
logger.addHandler(logging.StreamHandler())

OCS_STEM: str = r"ocs"
PDF_STEM = "bestiary"

OCS_HTML_PATH: Path = Path(f"ocs/{OCS_STEM}.html")
OCS_YAML_PATH: Path = Path(f"ocs/{OCS_STEM}.yaml")

OCS_PDF_PATH: Path = Path(f"out/{PDF_STEM}.pdf")
OCS_CSS_BUILD_PATH: Path = Path(f"out/out.css")
OCS_HTML_JINJA2_PATH: Path = Path(f"out/jinja2.html")

PARENT = Path(__file__).absolute().parent


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
    art_fullbody_path: str
    art_width: str
    art_height: str
    art_side: str
    origin: list[str]
    pronouns: list[Pronouns]
    skill: int | None
    hd: int | None
    armor: int | None
    morale: int | None
    desc: str
    abils: list[str] = field(default_factory=list[str])

    @staticmethod
    def from_dict(d: dict, all_pronouns: dict) -> 'NPC':
        art_fullbody_filename = d.get('art_fullbody_filename', "")
        art_fullbody_path = ""
        if art_fullbody_filename:
            art_fullbody_path = "art/" + art_fullbody_filename

        npc = NPC(
            name=d['name'],
            origin=d.get('from', []),
            pronouns=[
                Pronouns.from_subject(p, all_pronouns) for p in d.get('pronouns', [])
            ],
            hd=d.get('hd', None),
            armor=d.get('armor', None),
            morale=d.get('morale', None),
            skill=d.get('skill', None),
            desc=d.get('desc', ""),
            abils=d.get('abils', []),
            art_fullbody_path=art_fullbody_path,
            art_width=d.get('art_width', '2in'),
            art_height=d.get('art_height', '2in'),
            art_side=d.get('art_side', 'right'),
        )
        npc.desc = str(markdown(npc.desc))
        npc.abils = [str(markdown(s)) for s in npc.abils]

        return npc


def command_jinja() -> None:
    html_raw: str = OCS_HTML_PATH.read_text(encoding='utf-8')
    template: Template = Template(html_raw)

    # yaml
    print('parsing YAML')
    data: dict = yaml.safe_load(OCS_YAML_PATH.open(encoding='utf-8'))
    ocs: list[NPC] = [
        NPC.from_dict(oc, data['pronouns']) for oc in data['ocs'] if not oc.get('skip')
    ]

    # jinja2
    print('running jinja2')
    data_dict: dict = {'bestiary': {'ocs': ocs}}
    html_rendered: str = template.render(data_dict)
    Path("out/jinja2.html").write_text(html_rendered)


def command_pdf(html_rendered: str) -> None:
    # css
    css_tailwind: CSS = CSS(string=OCS_CSS_BUILD_PATH.read_text())
    reset = CSS(string=Path("ocs/reset.css").read_text())

    # pdf
    print('writing PDF')
    HTML(
        string=html_rendered,
        encoding="utf-8",
        base_url=PARENT,
    ).write_pdf(OCS_PDF_PATH, stylesheets=[reset, css_tailwind])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('command')
    args = ap.parse_args()
    command: str = args.command

    match command:
        case 'jinja2':
            command_jinja()
        case 'pdf':
            command_pdf(OCS_HTML_JINJA2_PATH.read_text())
