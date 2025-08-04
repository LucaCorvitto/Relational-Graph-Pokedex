from flet import Paint, PaintingStyle, Colors
from flet.canvas import Path

def get_shperical_reflection(radius : int) -> Path:
    """
    Creates a reflecton for a sphere/hemisphere of radius RADIUS
    returns a Path to be used for a Canvas
    """

    starting_point = radius*0.2

    return Path(
                [
                    Path.MoveTo(starting_point, starting_point),
                    Path.QuadraticTo(starting_point*2, starting_point/5, starting_point*3, starting_point/2, 0.5),
                    Path.QuadraticTo(starting_point/2, starting_point, starting_point/2, starting_point*3, 0.8),
                    Path.QuadraticTo(starting_point/5, starting_point, starting_point, starting_point, 0.5),
                ],
                paint=Paint(
                    stroke_width=2,
                    style=PaintingStyle.FILL,
                    color=Colors.with_opacity(0.5, Colors.WHITE),
                ),
            )

if __name__ == "__main__":
    from flet import Page, app
    from flet.canvas import Canvas
    def main(page: Page):

        page.window.width = 300
        page.window.height = 300
        page.bgcolor = "black"
        page.add(
            Canvas(
                [get_shperical_reflection(200)],
            
            width=float("inf"),
            expand=True
            )
        )

    app(main)