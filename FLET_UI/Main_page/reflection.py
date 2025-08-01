import flet as ft
import flet.canvas as cv

def get_shperical_reflection(radius):

    starting_point = radius*0.2

    return cv.Path(
                [
                    cv.Path.MoveTo(starting_point, starting_point),
                    cv.Path.QuadraticTo(starting_point*2, starting_point/5, starting_point*3, starting_point/2, 0.5),
                    cv.Path.QuadraticTo(starting_point/2, starting_point, starting_point/2, starting_point*3, 0.8),
                    cv.Path.QuadraticTo(starting_point/5, starting_point, starting_point, starting_point, 0.5),
                ],
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.FILL,
                    color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE),
                ),
            )

if __name__ == "__main__":
    def main(page: ft.Page):

        page.window.width = 150
        page.window.height = 150
        page.bgcolor = "grey"
        page.add(
            cv.Canvas(
                [get_shperical_reflection(200)],
            
            width=float("inf"),
            expand=True
            )
        )

    ft.app(main)