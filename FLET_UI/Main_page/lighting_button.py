import asyncio
import flet as ft
import flet.canvas as cv

import os, sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Main_page.reflection import get_shperical_reflection
from FLET_UI.Custom_elements.lighten_color import lighten_color


class lighting_button(ft.Container):
    def __init__(
            self,
            radius: int,
            color: str | ft.Colors = "grey",
            border_color: str | ft.Colors = "white",
            do_blink : bool = False
        ):

        super().__init__()

        self.do_blink = do_blink
        self.blink_task = None

        self.width = self.height = radius
        
        border = ft.Border(
            top= ft.BorderSide(
                width=radius/15,
                color= border_color,
            ),
            bottom= ft.BorderSide(
                width=radius/15,
                color= border_color,
            ),
            left= ft.BorderSide(
                width=radius/15,
                color= border_color,
            ),
            right= ft.BorderSide(
                width=radius/15,
                color= border_color,
            ),
        )

        self.light_button = ft.Container(
            width= radius,
            height=radius,
            bgcolor=color,
            border= border,
            border_radius= 100
        )

        self.light_color = color
        
        self.reflection = get_shperical_reflection(radius)

        self.content = ft.Stack(
            [self.light_button,
             self.reflection]
        )

    
    async def blink(self):
        while True:
            await asyncio.sleep(1)
            self.light_button.bgcolor = lighten_color(self.light_color)
            self.update()
            await asyncio.sleep(0.1)
            self.light_button.bgcolor = self.light_color
            self.update()
    
    #to start and stop the blinking process
    def did_mount(self):
        if self.do_blink:
            self.blink_task = self.page.run_task(self.blink)
    
    def will_unmount(self):
        # This is called when the control is removed from the page
        if self.blink_task:
            self.blink_task.cancel()

if __name__ == "__main__":
    def main(page: ft.Page):
        page.bgcolor = "grey"
        row = ft.Row([
            lighting_button(radius= 100, color= "red", do_blink= True),
            lighting_button(radius= 50, color= "blue", border_color= "black"),
            lighting_button(radius= 50, color= "green", border_color= "black" )
        ])
        page.add(row)

    ft.app(target=main)