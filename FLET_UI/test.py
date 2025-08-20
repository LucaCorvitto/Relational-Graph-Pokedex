import flet as ft
import flet.canvas as cv
import math
import random

def draw_graph(page: ft.Page, nodes, edges):
    page.title = "Neo4j Graph Viewer"
    page.scroll = "auto"
    page.update()

    # --- parameters ---
    radius = 200
    center_x, center_y = 400, 300
    node_radius = 20

    # --- assign positions ---
    angle_step = 2 * math.pi / len(nodes) if nodes else 1
    positions = {}
    for i, node in enumerate(nodes):
        angle = i * angle_step
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        positions[node["id"]] = (x, y)

    # --- create canvas ---
    canvas = cv.Canvas(
        [
            # draw edges
            *[
                cv.Line(
                    positions[edge["from"]][0],
                    positions[edge["from"]][1],
                    positions[edge["to"]][0],
                    positions[edge["to"]][1],
                    paint=ft.Paint(color="grey", stroke_width=2),
                )
                for edge in edges
                if edge["from"] in positions and edge["to"] in positions
            ],
            # edge labels with offset
            *[
                (
                    lambda x1, y1, x2, y2, label: cv.Text(
                        text=label,
                        x=(x1 + x2) / 2 + (- (y2 - y1) / math.sqrt((x2 - x1)**2 + (y2 - y1)**2)) * 15,
                        y=(y1 + y2) / 2 + ((x2 - x1) / math.sqrt((x2 - x1)**2 + (y2 - y1)**2)) * 15,
                        style=ft.TextStyle(size=12, color="black"),
                    )
                )(
                    positions[edge["from"]][0],
                    positions[edge["from"]][1],
                    positions[edge["to"]][0],
                    positions[edge["to"]][1],
                    edge["label"],
                )
                for edge in edges
                if edge["from"] in positions and edge["to"] in positions
            ],
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
            # node labels
            *[
                cv.Text(
                    text=node["label"],
                    x=positions[node["id"]][0] - 10,
                    y=positions[node["id"]][1] - node_radius - 15,
                    style=ft.TextStyle(size=12, color="black", weight="bold"),
                )
                for node in nodes
            ],
        ],
        width=800,
        height=600,
    )

    page.add(canvas)

# --- Flet entrypoint ---
def main(page: ft.Page):
    # Example data (replace with your Neo4j query results)
    nodes = [
        {"id": 1, "label": "Pichu", "group": "Pokemon"},
        {"id": 2, "label": "Pikachu", "group": "Pokemon"},
        {"id": 3, "label": "Raichu", "group": "Pokemon"},
        {"id": 4, "label": "Electric", "group": "Type"},
    ]
    edges = [
        {"from": 2, "to": 4, "label": "HAS_TYPE"},
        {"from": 2, "to": 1, "label": "EVOLVES_FROM"},
        {"from": 2, "to": 3, "label": "EVOLVES_TO"},
    ]

    draw_graph(page, nodes, edges)

ft.app(target=main)
