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
    def __init__(self, color: ft.Colors = "blue", width = 80, heigth = 80, shadow_offset: float = 5.0):
        super().__init__(expand=True)
        self.shadow_offset = shadow_offset
        self.color = color
        self.heigth = heigth
        self.width = width

    def draw_path(self, y_offset=0, width_limit = 170):

        #width limit is needed to keep the space for the lights.
        if width_limit >0:
            width = self.width/3 if self.width/3 > width_limit else width_limit

        return [
            cv.Path.LineTo(0, self.height + y_offset),
            cv.Path.LineTo(width, self.height + y_offset),
            cv.Path.LineTo((width) +30, self.height -20 + y_offset),
            cv.Path.LineTo(self.width, self.height -20 + y_offset),
            cv.Path.LineTo(self.width, 0 + y_offset),
            cv.Path.Close(),
        ]

    def draw_zigzag(self, width, height, e=None):
        self.shapes = []

        self.width = width
        self.height = height

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
        shadow_path = [cv.Path.MoveTo(0, self.height * 3/ 8 + self.shadow_offset)]
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

#=============================================================================================

class TopNavigationPokedex(ft.Container):
    def  __init__(
            self,
            title: Optional[str] = "Pokedex",
            color : Optional[ft.Colors] = "red",
            height_page_ratio = 1/8,
            on_submit_query : Optional[callable] = None,
            on_expand_query : Optional[callable] = None,
        ):
        
        self.min_height = 80
        self.height_page_ratio = height_page_ratio

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

        self.invisi_container = ft.Container(
            height=80,
            bgcolor= ft.Colors.with_opacity(0, "black"),
            padding= 10,
            content= header,
            alignment= ft.alignment.bottom_center
        )

        self.outline = PokedexTopShape(color=color)
        
        self.structure = ft.Stack([
            self.outline,
            self.invisi_container
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

    def _update_children(self, e = None):
        height = self.page.height * self.height_page_ratio

        height = height if height > self.min_height else self.min_height

        self.width = self.page.width
        self.height = height
        self.outline.draw_zigzag(width= self.width, height= self.height)
        self.outline.update()
        self.invisi_container.height = self.height -10
        self.invisi_container.update()
        self.update()


    def did_mount(self):
        #make sure the control is at the top of the page
        self.page.controls.remove(self)
        self.page.controls.insert(0, self)
        self.page.overlay.append(self.structure)
        self.page.update()
        self._update_children()
        # Chain on_resized handlers
        previous_handler = self.page.on_resized

        def combined_handler(e):
            self._update_children(e)
            if previous_handler:
                previous_handler(e)

        self.page.on_resized = combined_handler

    def will_unmount(self):
        self.page.overlay.remove(self.structure)
        self.page.update()


if __name__ == "__main__":
    def main(page: ft.Page):
        poke = TopNavigationPokedex()
        page.add (poke)
        page.add(ft.TextField(hint_text="insert_query", on_submit= lambda _ : poke.show_query_field("lol")))

    ft.app(target=main)