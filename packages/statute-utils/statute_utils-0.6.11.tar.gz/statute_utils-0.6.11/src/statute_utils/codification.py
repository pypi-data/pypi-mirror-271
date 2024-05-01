import datetime
from collections.abc import Iterator
from pathlib import Path
from typing import Any, NamedTuple

import yaml  # type: ignore
from dateutil.parser import parse  # type: ignore

from .components import (
    create_fts_snippet_column,
    create_unit_heading,
    fetch_values_from_key,
    set_node_ids,
    walk,
)
from .main import extract_rule
from .models import Rule
from .templater import html_tree_from_hierarchy


class Codification(NamedTuple):
    """A instance is dependent on a specifically
    formatted codification Path, i.e.:

    ```<folder>/<statute-category>/<statute-id>/<specific-code-id>`

    The shape of the contents will be different
    from the shape of the dumpable `.yml` export."""

    title: str
    description: str
    date: datetime.date
    slug: str
    rule: Rule
    units: list[dict]

    def __str__(self) -> str:
        return f"code: {self.rule.__str__()}, {self.date.strftime('%b %d, %Y')}"

    def __repr__(self) -> str:
        return "/".join([self.rule.cat.value, self.rule.num, self.slug])

    @classmethod
    def from_file(cls, file: Path):
        data = yaml.safe_load(file.read_bytes())

        base = data.get("base")
        if not base:
            return None

        rule = extract_rule(base)
        if not rule:
            return None

        title = data.get("title")
        if not title:
            return None

        description = data.get("description")
        if not description:
            return None

        dt = data.get("date")
        if not dt:
            return None

        return cls(
            title=title,
            description=description,
            date=parse(dt).date(),
            slug=file.stem,
            rule=rule,
            units=data.get("units"),
        )

    def prepare_root(self):
        """Adds material paths to each node in the tree with the root
        node given special features: it's marked with a material path `id`
        of `1.`"""
        set_node_ids(self.units)
        root = {"id": "1.", "units": self.units}
        return [root]

    def make_row(self) -> dict:
        """See same logic in Statute."""
        units = self.prepare_root()
        fts = self.flatten_units(self.slug, units)  # excludes the root
        html = html_tree_from_hierarchy(units[0]["units"])  # excludes root
        return {
            "id": self.slug,
            "title": self.title,
            "description": self.description,
            "cat": self.rule.cat.value,
            "num": self.rule.num,
            "date": self.date,
            "units": units,
            "fts": fts,
            "html": html,
        }

    @classmethod
    def flatten_units(
        cls, codification_id: str, units: list[dict[str, Any]], heading: str = ""
    ) -> Iterator[dict[str, str | None]]:
        """See same logic in Statute."""
        for unit in units:
            present_heading = create_unit_heading(unit, heading)
            yield {
                "codification_id": codification_id,
                "material_path": unit["id"],  # enable subtree
                "heading": present_heading,  # identify subtree
                "item": unit.get("item"),
                "caption": unit.get("caption"),
                "content": unit.get("content"),
                "snippetable": create_fts_snippet_column(unit),  # enable searchability
            }
            if subunits := unit.get("units"):
                yield from cls.flatten_units(codification_id, subunits, present_heading)

    def extract_events(self):
        """Each unit in a codification may contain a history."""
        data = {"units": self.units}
        histories = fetch_values_from_key(data=data, key="history")
        for history in histories:
            for event in history:
                yield event
