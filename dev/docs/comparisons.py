"""Render measured values as accessible, selectable comparison charts."""
from typing import NamedTuple

LOGOS = {
    "podbag": "images/logo-small.png", "docker": "logos/docker.svg",
    "podman": "logos/podman.svg", "kiri": "logos/kiri.svg",
    "orbstack": "logos/orbstack.png", "colima": "logos/colima.png",
}


class Reading(NamedTuple):
    product: str
    label: str        # Rendered label, including the mode or revision if applicable.
    magnitude: float  # All readings in one chart use the same unit.
    display: str      # Localized value with its original unit.


class Metric(NamedTuple):
    name: str
    rows: list[Reading]
    caption: str = ""


def series(rows, root):
    maximum = max(r.magnitude for r in rows)
    cells = []
    for row in rows:
        width = 100 * row.magnitude / maximum if maximum else 0
        cells.append(
            f'<span class="fact-brand"><img class="logo-{row.product}" src="{root}{LOGOS[row.product]}" '
            f'width="22" height="22" alt=""><span>{row.label}</span></span>'
            f'<span class="fact-track" aria-hidden="true"><span class="fact-bar {row.product}-bar" '
            f'style="width:{width:.4f}%"></span></span><strong>{row.display}</strong>')
    return '<div class="fact-series">' + "\n".join(cells) + '</div>'


def chart(metric, root):
    note = f"<small>{metric.caption}</small>" if metric.caption else ""
    return (f'<figure class="comparison-card reveal"><figcaption>{metric.name}{note}</figcaption>'
            f'{series(metric.rows, root)}</figure>')


def picker(name, legend, metrics, root):
    if len(metrics) == 1:
        return chart(metrics[0], root)
    panels = []
    for i, metric in enumerate(metrics, 1):
        control = f"{name}-{i}"
        caption = f'<figcaption>{metric.caption}</figcaption>' if metric.caption else ""
        checked = " checked" if i == 1 else ""
        panels.append(
            f'<input class="sr-only" type="radio" name="{name}" id="{control}" '
            f'aria-controls="{control}-result"{checked}>'
            f'<label id="{control}-label" for="{control}">{metric.name}</label>'
            f'<figure class="fact-result" id="{control}-result" aria-labelledby="{control}-label">'
            f'{caption}{series(metric.rows, root)}</figure>')
    cols = 3 if len(metrics) == 5 else min(4, len(metrics))
    return (f'<fieldset class="facts comparisons reveal" style="--columns:{cols}">'
            f'<legend class="sr-only">{legend}</legend><div class="facts-grid">'
            + "\n".join(panels) + '</div></fieldset>')
