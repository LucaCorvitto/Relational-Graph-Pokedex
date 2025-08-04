import asyncio
from flet import Colors, Container,  Stack, Border, BorderSide
from flet.canvas import Canvas

import os, sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Main_page.reflection import get_shperical_reflection
from FLET_UI.Custom_elements.lighten_color import lighten_color


class lighting_button(Container):
    def __init__(
        self,
        radius: int,
        color: str | Colors = "grey",
        border_color: str | Colors = "white",
        do_blink: bool = False
    ):
        super().__init__()

        self.do_blink = do_blink
        self.blink_task = None
        self.blinking = False
        self.current_frequency = 1.0

        self._radius = radius
        self.inner_border_color = border_color

        self.width = self.height = radius

        self.inner_border = self.create_border(radius= radius, border_color=border_color)

        self.light_button = Container(
            width=radius,
            height=radius,
            bgcolor=color,
            border=self.inner_border,
            border_radius=100
        )

        self.light_color = color
        self.reflection = Canvas(
            [get_shperical_reflection(radius)],
            width=float("inf"),
            expand=True
        )

        self.content = Stack([
            self.light_button,
            self.reflection
        ])

    def create_border(self, radius, border_color) -> Border:
        return Border(
            top=BorderSide(width=radius / 15, color=border_color),
            bottom=BorderSide(width=radius / 15, color=border_color),
            left=BorderSide(width=radius / 15, color=border_color),
            right=BorderSide(width=radius / 15, color=border_color),
        )

    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value: int):
        self._radius = value
        self.light_button.height = value
        self.light_button.width = value
        self.height = value
        self.width = value
        self.inner_border = self.create_border(value, self.inner_border_color)
        self.reflection.shapes = [get_shperical_reflection(value)]
        self.reflection.update()
        
    async def _blink(self):
        while True:
            await asyncio.sleep(self.current_frequency)
            self.light_button.bgcolor = lighten_color(self.light_color)
            self.update()
            await asyncio.sleep(0.1)
            self.light_button.bgcolor = self.light_color
            self.update()

    def start_blinking(self, frequency: float = 1.0):
        if not self.blinking:
            self.blinking = True
            self.current_frequency = frequency
            self.blink_task = self.page.run_task(self._blink)

    def update_blinking_frequency(self, frequency: float):
        if self.blinking:
            self.stop_blinking()
            self.start_blinking(frequency)

    def stop_blinking(self):
        if self.blink_task:
            self.blink_task.cancel()
            self.blink_task = None
        self.blinking = False

    def did_mount(self):
        if self.do_blink:
            self.start_blinking()

    def will_unmount(self):
        self.stop_blinking()

if __name__ == "__main__":
    from flet import Page, Row, app
    def main(page: Page):
        page.bgcolor = "grey"
        row = Row([
            lighting_button(radius= 100, color= "red", do_blink= True),
            lighting_button(radius= 50, color= "blue", border_color= "black"),
            lighting_button(radius= 50, color= "green", border_color= "black" )
        ])
        page.add(row)

    app(target=main)