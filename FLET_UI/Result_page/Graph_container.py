import flet as ft
import flet.canvas as cv
import math
from typing import ClassVar

def _draw_arrow(x2, y2, dx, dy, size=10, thickness = 3, color = ft.Colors.GREY_500):
    """Draw arrowhead at (x2,y2) pointing along (dx,dy)."""
    size = max(size, thickness*5)
    length = math.sqrt(dx * dx + dy * dy)
    if length == 0:
        return []
    ux, uy = dx / length, dy / length
    px, py = -uy, ux

    bx, by = x2 - ux * size, y2 - uy * size
    left = (bx + px * size * 0.5, by + py * size * 0.5)
    right = (bx - px * size * 0.5, by - py * size * 0.5)

    return [
        cv.Line(x2, y2, left[0], left[1], paint=ft.Paint(color=color, stroke_width=thickness)),
        cv.Line(x2, y2, right[0], right[1], paint=ft.Paint(color=color, stroke_width=thickness)),
    ]

def _draw_curved_edge(x1, y1, x2, y2, label, thickness=3, color=ft.Colors.GREY_500, text_size=12, target_radius=10):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    length = math.sqrt(dx * dx + dy * dy)
    if length == 0:
        return []

    px, py = -dy / length, dx / length
    bend = min(length * 0.15, 40)
    cx, cy = mx + px * bend, my + py * bend

    # --- NEW: shorten endpoint so it lands on circumference ---
    # tangent vector at end of curve (P1 - C)
    tx, ty = x2 - cx, y2 - cy
    tlen = math.sqrt(tx * tx + ty * ty)
    if tlen != 0:
        tx, ty = tx / tlen, ty / tlen
        # move point backwards by target_radius
        end_x = x2 - tx * target_radius
        end_y = y2 - ty * target_radius
    else:
        end_x, end_y = x2, y2

    return [
        cv.Path(
            [
                cv.Path.MoveTo(x1, y1),
                cv.Path.QuadraticTo(cx, cy, end_x, end_y),  # use shifted end
            ],
            paint=ft.Paint(
                color=color,
                stroke_width=thickness,
                style=ft.PaintingStyle.STROKE,
            ),
        ),
        cv.Text(
            text=label,
            x=cx,
            y=cy,
            style=ft.TextStyle(size=text_size, color="black"),
        ),
        *_draw_arrow(end_x, end_y, end_x - cx, end_y - cy, thickness=thickness),
    ]


class GraphDrawing(ft.Container):

    MinRadius: ClassVar[int] = 50

    def draw_graph(
        self,
        nodes,
        edges,
        radius=200,
    ) -> cv.Canvas:
        # --- parameters ---
        radius = radius if radius > type(self).MinRadius else type(self).MinRadius
        center_x = center_y = 0
        node_radius = int(radius / 10)
        arrow_thickness = max(math.ceil(radius/50), 2)
        text_size= int(max(radius/15, 11))

        # --- assign positions ---
        angle_step = 2 * math.pi / len(nodes) if nodes else 1
        positions = {}
        for i, node in enumerate(nodes):
            angle = i * angle_step
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            positions[node["id"]] = (x, y)

        # --- create canvas ---
        return cv.Canvas(
            [
                # draw nodes
                *[
                    cv.Circle(
                        positions[node["id"]][0],
                        positions[node["id"]][1],
                        node_radius,
                        paint=ft.Paint(color="blue"),
                    )
                    for node in nodes
                ],
                # curved edges with arrows
                *[
                    elem
                    for edge in edges
                    if edge["from"] in positions and edge["to"] in positions
                    for elem in _draw_curved_edge(
                        positions[edge["from"]][0],
                        positions[edge["from"]][1],
                        positions[edge["to"]][0],
                        positions[edge["to"]][1],
                        edge["label"],
                        thickness= arrow_thickness,
                        text_size= text_size,
                        target_radius= node_radius
                    )
                ],
                # node labels
                *[
                    cv.Text(
                        text=node["label"],
                        x=positions[node["id"]][0] - 10,
                        y=positions[node["id"]][1] - node_radius - 15,
                        style=ft.TextStyle(size=text_size, color="black", weight="bold"),
                    )
                    for node in nodes
                ],
            ]
        )

    def __init__(self, nodes, edges, radius=200):
        super().__init__(
            content=self.draw_graph(nodes, edges, radius),
            height=radius * 3,
            width=radius * 4,
            alignment=ft.alignment.center,
            bgcolor="green",
            border_radius= radius*2
        )


# --- Flet entrypoint ---
def main(page: ft.Page):
    nodes = [
        {"id": 1, "label": "Pichu", "group": "Pokemon"},
        {"id": 2, "label": "Pikachu", "group": "Pokemon"},
        {"id": 3, "label": "Raichu", "group": "Pokemon"},
        {"id": 4, "label": "Electric", "group": "Type"},
    ]
    edges = [
        {"from": 2, "to": 4, "label": "HAS_TYPE"},
        {"from": 1, "to": 2, "label": "EVOLVES_FROM"},
        {"from": 2, "to": 3, "label": "EVOLVES_TO"},
    ]

    graph = GraphDrawing(nodes, edges)
    slider_value = ft.Text("100")
    def change_graph_radius(e):
        nonlocal graph
        page.remove(graph)
        graph = GraphDrawing(nodes, edges, radius= e.control.value)
        slider_value.value = e.control.value
        slider_value.update()
        page.add(graph)

    page.add(slider_value)
    page.add(ft.Slider(value= 100, min= 40, max= 500, divisions= 500, on_change= change_graph_radius))
    page.add(graph)


ft.app(target=main)
