from typing import Optional
import flet as ft
import flet.canvas as cv

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Custom_elements.text_decorator import Text_decorator
from FLET_UI.Main_page.lighting_button import lighting_button

#POKEDEX SHAPE------------------------------------------------------
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

        self.width = self.page.width

        # Main shape
        path_commands = [cv.Path.MoveTo(0, 0)]
        path_commands.extend(self.draw_path())

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
#=============================================================================================

class TopNavigationPokedex(ft.Container):
    def  __init__(
            self,
            title: Optional[str] = "Pokedex",
            color : Optional[ft.Colors] = "red",
            on_submit_query : Optional[callable] = None,
            on_expand_query : Optional[callable] = None,
        ):

        self.light_buttons = ft.Row( [
            ft.Divider(),
            lighting_button(50, "Blue", do_blink= True),
            lighting_button(25, "red"),
            lighting_button(25, "yellow"),
            lighting_button(25, "green"),
            ] )
        
        self.title = Text_decorator(title)

        self.query_field = ft.TextField(
            value="previous_query",
            suffix= ft.IconButton(ft.Icons.SEND, on_click= on_submit_query),
            prefix= ft.IconButton(ft.Icons.EXPAND, on_click= on_expand_query),
            bgcolor= ft.Colors.GREY_300,
            visible= False,
            multiline= True
            )

        header = ft.Row(
            [
                self.light_buttons,
                self.title,
                self.query_field
            ],
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True
        )

        invisi_container = ft.Container(
            height=80,
            bgcolor= ft.Colors.with_opacity(0, "black"),
            padding= 10,
            content= header,
        )
        
        self.structure = ft.Stack([
            PokedexTopShape(color=color),
            invisi_container
        ])

        super().__init__(
            content= ft.Text("This is TopNavigationPokedex placeholder"),
            height= 50
        )

    def show_query_field(self, query: Optional[str] = None):
        self.query_field.value = query
        self.query_field.visible = True
        self.query_field.update()
    
    def hide_query_field(self):
        self.query_field.visible = False
        self.query_field.update()

    def did_mount(self):
        self.page.controls.remove(self)
        self.page.controls.insert(0, self)
        self.page.overlay.append(self.structure)
        self.page.update()

    def will_unmount(self):
        self.page.overlay.remove(self.structure)
        self.page.update()


if __name__ == "__main__":
    def main(page: ft.Page):
        poke = TopNavigationPokedex()
        page.add (poke)
        page.add(ft.TextField(hint_text="insert_query", on_submit= lambda _ : poke.show_query_field("lol")))

    ft.app(target=main, view= ft.AppView.WEB_BROWSER)