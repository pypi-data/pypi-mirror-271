"""Artifact item."""

from gaphor import UML
from gaphor.core.modeling.properties import attribute
from gaphor.diagram.presentation import Classified, ElementPresentation
from gaphor.diagram.shapes import Box, cairo_state, draw_border
from gaphor.diagram.support import represents
from gaphor.UML.classes.stereotype import stereotype_compartments, stereotype_watches
from gaphor.UML.compartments import name_compartment


@represents(UML.Artifact)
class ArtifactItem(Classified, ElementPresentation):
    def __init__(self, diagram, id=None):
        super().__init__(diagram, id)

        self.watch("show_stereotypes", self.update_shapes)
        self.watch("subject[NamedElement].name")
        self.watch("subject[NamedElement].namespace.name")
        self.watch("children", self.update_shapes)
        stereotype_watches(self)

    show_stereotypes: attribute[int] = attribute("show_stereotypes", int)

    def update_shapes(self, event=None):
        self.shape = Box(
            name_compartment(self, draw_icon=draw_artifact_icon),
            *(self.show_stereotypes and stereotype_compartments(self.subject) or []),
            draw=draw_border,
        )


def draw_artifact_icon(box, context, bounding_box):
    with cairo_state(context.cairo) as cr:
        cr.set_line_width(1.0)
        ear = 5
        w = 15
        icon_margin_x = 6
        ix = bounding_box.width - icon_margin_x - w
        icon_margin_y = 12

        iy = icon_margin_y

        cr.move_to(ix + w - ear, iy)
        h = 20
        for x, y in (
            (ix + w - ear, iy + ear),
            (ix + w, iy + ear),
            (ix + w - ear, iy),
            (ix, iy),
            (ix, iy + h),
            (ix + w, iy + h),
            (ix + w, iy + ear),
        ):
            cr.line_to(x, y)
        stroke_color = context.style["color"]
        cr.set_source_rgba(*stroke_color)
        cr.stroke()
