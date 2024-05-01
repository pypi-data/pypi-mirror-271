from __future__ import annotations

import logging
from typing import Callable

from gaphas.geometry import Rectangle
from gaphas.item import NW, SE
from generic.multidispatch import FunctionDispatcher, multidispatch

from gaphor.core.modeling import Diagram, Element, Presentation
from gaphor.diagram.group import group, ungroup
from gaphor.diagram.presentation import ElementPresentation
from gaphor.diagram.support import get_diagram_item
from gaphor.UML.recipes import owner_package

log = logging.getLogger(__name__)


def drop_element(
    element: Element, diagram: Diagram, x: float, y: float
) -> Presentation | None:
    if item_class := get_diagram_item(type(element)):
        item = diagram.create(item_class)
        assert item

        item.matrix.translate(x, y)
        item.subject = element

        return item
    return None


drop: FunctionDispatcher[Callable[[Element, Element], bool]] = multidispatch(
    Element, Diagram
)(drop_element)


@drop.register(Presentation, Diagram)
def drop_presentation(item: Presentation, diagram: Diagram, x: float, y: float):
    if item.diagram is not diagram:
        return

    old_parent = item.parent

    if old_parent and ungroup(old_parent.subject, item.subject):
        item.change_parent(None)
        old_parent.request_update()


@drop.register(Presentation, Presentation)
def drop_on_presentation(
    item: Presentation, new_parent: Presentation, x: float, y: float
):
    """Place :obj:`item`, with position :obj:`pos` relative to :obj:`new_parent`."""
    assert item.diagram is new_parent.diagram

    old_parent = item.parent

    if new_parent is old_parent:
        if old_parent is not None:
            old_parent.request_update()
        return

    if old_parent and ungroup(old_parent.subject, item.subject):
        item.change_parent(None)
        old_parent.request_update()

    if new_parent and item.subject and group(new_parent.subject, item.subject):
        grow_parent(new_parent, item)
        item.change_parent(new_parent)
    elif item.subject:
        diagram_parent = owner_package(item.diagram)
        group(diagram_parent, item.subject)


def grow_parent(parent: Presentation, item: Presentation) -> None:
    if not isinstance(item, ElementPresentation):
        return

    if not isinstance(parent, ElementPresentation):
        log.warning(f"Can not grow item {parent}: not an ElementPresentation")
        return

    parent_bb = _bounds(parent)
    item_bb = _bounds(item)
    item_bb.expand(20)
    new_parent_bb = parent_bb + item_bb

    c2i = parent.matrix_i2c.inverse()
    parent.handles()[NW].pos = c2i.transform_point(new_parent_bb.x, new_parent_bb.y)
    parent.handles()[SE].pos = c2i.transform_point(new_parent_bb.x1, new_parent_bb.y1)


def _bounds(item: ElementPresentation) -> Rectangle:
    transform = item.matrix_i2c.transform_point
    x0, y0 = transform(*item.handles()[NW].pos)
    x1, y1 = transform(*item.handles()[SE].pos)
    return Rectangle(x0, y0, x1=x1, y1=y1)
