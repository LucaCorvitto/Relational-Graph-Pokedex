import flet as ft

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Custom_elements.text_decorator import Text_decorator
from FLET_UI.Main_page.lighting_button import lighting_button
from FLET_UI.Main_page.Top_navigation import TopNavigationPokedex

class Main_structure(ft.Container):
    def __init__(self):
        super().__init__(expand=True)

        self.content = ft.Column([
            ft.Row([
                ft.Column(
                    [
                        ft.Divider(),
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
        
if __name__ == "__main__":
    def main(page: ft.Page):
        page.add(TopNavigationPokedex())
        page.add(Main_structure())

        page.update()

    ft.app(target=main)