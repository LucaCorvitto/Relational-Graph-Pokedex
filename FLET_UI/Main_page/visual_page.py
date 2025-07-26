import flet as ft

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Custom_elements.text_decorator import Text_decorator
from FLET_UI.Main_page.lighting_button import lighting_button


class Top_navigation(ft.Container):
    def  __init__(self):
        
        border_radius=ft.border_radius.only(
            top_left=0, top_right=0, bottom_left=15, bottom_right=15
        ),  # only round top corners
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 5)  # push shadow downward
        ),

        super().__init__(
            height=80,
            bgcolor= "yellow",
            shadow= shadow,
            #border_radius= border_radius
        )

class Top_navigation_placeholder(ft.Container):
    def  __init__(self):
        
        super().__init__(
            height=70,
        )
                
        self.light_buttons = [
            lighting_button(50, "Blue", do_blink= True),
            lighting_button(25, "red"),
            lighting_button(25, "yellow"),
            lighting_button(25, "green"),
            ]
        
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
                Top_navigation(),
            ]
        )

        self.content = overlay

if __name__ == "__main__":
    def main(page: ft.Page):
        page.add(Main_structure())

        page.update()

    ft.app(target=main)