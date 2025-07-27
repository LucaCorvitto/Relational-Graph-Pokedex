import flet as ft
import flet.canvas as cv

class PokedexTopShape(cv.Canvas):
    def __init__(self, color: ft.Colors = "blue", height : int = 90, shadow_offset: float = 5.0):
        super().__init__(expand=True)
        self.shadow_offset = shadow_offset
        self.color = color
        self.height = height

    def draw_path(self, y_offset=0):
        return [
            cv.Path.LineTo(0, self.height *0.8 + y_offset),
            cv.Path.LineTo(self.width * 2 / 3, self.height *0.8 + y_offset),
            cv.Path.LineTo(self.width * 3 / 4, self.height + y_offset),
            cv.Path.LineTo(self.width, self.height + y_offset),
            cv.Path.LineTo(self.width, 0 + y_offset),
            cv.Path.Close(),
        ]

    def draw_zigzag(self, e=None):
        self.shapes = []

        self.width = self.page.window.width

        # Main shape
        path_commands = [cv.Path.MoveTo(0, 0)]
        path_commands.extend(self.draw_path())  # FIXED HERE

        self.shapes.append(
            cv.Path(
                path_commands,
                paint=ft.Paint(
                    stroke_width=3,
                    style=ft.PaintingStyle.STROKE,
                    color=ft.Colors.BLACK,
                ),
            )
        )

        self.shapes.append(
            cv.Path(
                path_commands,
                paint=ft.Paint(
                    style=ft.PaintingStyle.FILL,
                    color=self.color,
                ),
            )
        )

        # Shadow
        shadow_path = [cv.Path.MoveTo(0, self.height / 8 + self.shadow_offset)]
        shadow_path.extend(self.draw_path(y_offset=self.shadow_offset))  # FIXED HERE

        self.shapes.append(
            cv.Path(
                shadow_path,
                paint=ft.Paint(
                    style=ft.PaintingStyle.FILL,
                    color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                ),
            )
        )

        self.update()

    def did_mount(self):
        self.draw_zigzag()
        self.page.on_resized = self.draw_zigzag  # Correct handler assignment
        self.page.update()

if __name__ == "__main__":

    def main(page: ft.Page):
        page.bgcolor = ft.Colors.WHITE
        page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        page.vertical_alignment = ft.MainAxisAlignment.START

        zigzag_canvas = PokedexTopShape()
        page.add(zigzag_canvas)

    ft.app(main)
