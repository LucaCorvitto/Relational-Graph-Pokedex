import flet as ft
import flet.canvas as cv

lol = cv.Canvas(
        [
            cv.Path(
                [
                    cv.Path.MoveTo(17, 17),
                    cv.Path.QuadraticTo(30, 0, 50, 10, 0.5),
                    cv.Path.QuadraticTo(10, 15, 10, 50, 0.8),
                    cv.Path.QuadraticTo(0, 20, 17, 17, 0.5),
                ],
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.FILL,
                    color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE),
                ),
            ),
        ],
        width=float("inf"),
        expand=True,
)

def get_shperical_reflection(radius):

    starting_point = radius*0.2

    return cv.Canvas(
        [
            cv.Path(
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
            ),
        ],
        width=float("inf"),
        expand=True,
    )

if __name__ == "__main__":
    def main(page: ft.Page):

        page.window.width = 150
        page.window.height = 150
        page.bgcolor = "grey"
        page.add(get_shperical_reflection(200))

    ft.app(main)