import flet as ft

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Custom_elements.text_decorator import Text_decorator
from FLET_UI.Main_page.lighting_button import lighting_button
from FLET_UI.Main_page.pokedex_top import PokedexTopShape


class Top_navigation(ft.Container):
    def  __init__(self):

        self.light_buttons = ft.Row( [
            lighting_button(50, "Blue", do_blink= True),
            lighting_button(25, "red"),
            lighting_button(25, "yellow"),
            lighting_button(25, "green"),
            ] )

        super().__init__(
            height=80,
            bgcolor= ft.Colors.with_opacity(0, "black"),
            padding= 10,
            #border_radius= border_radius,
            content= self.light_buttons
        )

class Top_navigation_placeholder(ft.Container):
    def  __init__(self):
        
        super().__init__(
            height=70,
        )
        
        self.bgcolor = "green"


class Main_structure(ft.Container):
    def __init__(self):
        super().__init__(expand=True)

        structure = ft.Column([
            Top_navigation_placeholder(),
            ft.Row([
                ft.Column(
                    [
                        ft.Container(width= 120, height=180, bgcolor="red"),
                        ft.Container(width=120, height=180, bgcolor="red"),
                        ft.Container(width=120, height=180, bgcolor="red"),
                        ft.Container(width=120, height=180, bgcolor="red")
                    ],
                    scroll= "always",
                    expand_loose= True
                ),
                ft.Divider(),
                ft.Container(bgcolor= "blue", expand= True)
                ],
                expand=True,
                vertical_alignment= ft.CrossAxisAlignment.START,
            )],
            spacing=0
            )
        
        overlay = ft.Stack(
            [
                structure,
                PokedexTopShape(ft.Colors.BLUE_ACCENT_400),
                Top_navigation(),
            ]
        )

        self.content = overlay

if __name__ == "__main__":
    def main(page: ft.Page):
        page.add(Main_structure())

        page.update()

    ft.app(target=main)