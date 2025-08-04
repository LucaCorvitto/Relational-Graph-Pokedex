from flet import Colors, Paint, PaintingStyle
from flet.canvas import Canvas, Path

class PokedexShape(Canvas):
    def __init__(
        self,
        color: Colors | str = "blue",
        width_ratio: float = 0.5,
        width: float = 80,
        height: float = 80,
        shadow_offset: float = 5.0,
        width_limit: float = 170,
        flipped: bool = False,  # ⬅️ Invert the shape (top/bottom)
    ):
        super().__init__(expand=True)

        if not (0 <= width_ratio <= 1):
            raise ValueError("width_ratio must be between 0 and 1")

        self.color = color
        self.width = width
        self.height = height
        self.width_ratio = width_ratio
        self.shadow_offset = shadow_offset
        self.width_limit = width_limit
        self.flipped = flipped

    def draw_path(self, y_offset=0):
        w_ratio = self.width * self.width_ratio
        base_width = max(w_ratio, self.width_limit)
        height = self.height * 5

        if self.flipped:
            # Bottom shape (points upward)
            return [
                Path.LineTo(self.width, -y_offset),
                Path.LineTo(base_width + 30, -y_offset),
                Path.LineTo(base_width, 20 - y_offset),
                Path.LineTo(0, 20 - y_offset),
                Path.LineTo(0, height / 2 - y_offset) if y_offset else Path.LineTo(0, height),
                Path.Close(),
            ]
        else:
            # Top shape (points downward)
            return [
                Path.LineTo(0, self.height + y_offset),
                Path.LineTo(base_width, self.height + y_offset),
                Path.LineTo(base_width + 30, self.height - 20 + y_offset),
                Path.LineTo(self.width, self.height - 20 + y_offset),
                Path.LineTo(self.width, -self.height / 2 + y_offset) if y_offset else Path.LineTo(self.width, -self.height * 5),
                Path.Close(),
            ]

    def draw_zigzag(self, width, height, e=None):
        self.shapes = []
        self.width = width
        self.height = height

        if self.flipped:
            move_start = Path.MoveTo(self.width, self.height * 5)
        else:
            move_start = Path.MoveTo(0, -self.height * 5)

        path_commands = [move_start]
        path_commands.extend(self.draw_path())

        # Outline
        self.shapes.append(
            Path(
                path_commands,
                paint=Paint(
                    stroke_width=8,
                    style=PaintingStyle.STROKE,
                    color=Colors.BLACK38,
                ),
            )
        )

        # Fill
        self.shapes.append(
            Path(
                path_commands,
                paint=Paint(
                    style=PaintingStyle.FILL,
                    color=self.color,
                ),
            )
        )

        # Shadow
        if self.flipped:
            shadow_start = Path.MoveTo(self.width, -self.shadow_offset)
        else:
            shadow_start = Path.MoveTo(0, self.height * 9 / 10 + self.shadow_offset)

        shadow_path = [shadow_start]
        shadow_path.extend(self.draw_path(y_offset=self.shadow_offset))

        self.shapes.append(
            Path(
                shadow_path,
                paint=Paint(
                    style=PaintingStyle.FILL,
                    color=Colors.with_opacity(0.2, Colors.BLACK),
                ),
            )
        )

if __name__ == "__main__":
    from flet import Page, Column, Container, app
    def main(page: Page):
        page.scroll = "auto"

        # Create shapes
        shape_top = PokedexShape(color="red", flipped=False)
        shape_bottom = PokedexShape(color="blue", flipped=True)

        # Call draw manually before using them
        shape_top.draw_zigzag(300, 80)
        shape_bottom.draw_zigzag(300, 80)

        # Add them inside containers with fixed height
        page.add(
            Column(
                controls=[
                    Container(content=shape_top, height=200),
                    Container(content=shape_bottom, height=200),
                ]
            )
        )

    app(target= main)