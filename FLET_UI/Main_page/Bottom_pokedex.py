from typing import Optional
import flet as ft
import flet.canvas as cv

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Custom_elements.text_decorator import Text_decorator

#POKEDEX SHAPE------------------------------------------------------
class PokedexBottomShape(cv.Canvas):
    def __init__(
            self,
            color: ft.Colors = "blue",
            width_ratio = 2/3,
            width=80,
            heigth=80,
            shadow_offset: float = 5.0,
            width_limit=170,
        ):
        super().__init__(expand=True)
        if width_ratio < 0 or width_ratio > 1:
            raise ValueError("width_ratio must be between 0 and 1")

        self.shadow_offset = shadow_offset
        self.color = color
        self.heigth = heigth
        self.width = width
        self.width_limit = width_limit
        self.width_ratio = width_ratio

    def draw_path(self, y_offset=0):
        """
        Build the polygon path starting from the bottom and going upward.
        """
        if self.width_limit > 0:
            width_limit = self.width *self.width_ratio if self.width *self.width_ratio > self.width_limit else self.width_limit
        else:
            width_limit = 0

        h = self.height

        return [
            # from bottom-right, move left
            cv.Path.LineTo(self.width, - y_offset),  # top-right corner
            cv.Path.LineTo(width_limit + 30, - y_offset),  # slanted corner near top-left
            cv.Path.LineTo(width_limit,  20- y_offset),       # top-left section
            cv.Path.LineTo(0, 20- y_offset),                 # very top-left corner
            cv.Path.LineTo(0, h - y_offset),                 # bottom-left corner
            cv.Path.Close(),
        ]

    def draw_zigzag(self, width, height, e=None):
        self.shapes = []
        self.width = width
        self.height = height

        h = self.height

        # Start from bottom-right
        path_commands = [cv.Path.MoveTo(self.width, h)]
        path_commands.extend(self.draw_path())

        # Outline
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

        # Fill
        self.shapes.append(
            cv.Path(
                path_commands,
                paint=ft.Paint(
                    style=ft.PaintingStyle.FILL,
                    color=self.color,
                ),
            )
        )

        # Shadow (shift upward)
        shadow_path = [cv.Path.MoveTo(self.width, h - self.shadow_offset)]
        shadow_path.extend(self.draw_path(y_offset=self.shadow_offset))

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

class BottomPokedex(ft.Container):
    def  __init__(
            self,
            title: Optional[str] = "Pokedex",
            color : Optional[ft.Colors] = "red",
            height_page_ratio : float = 1/8,
            width_page_ratio : float = 1/2,
            overlap : int = 25,
        ):
        
        if height_page_ratio < 0 or height_page_ratio > 1:
            raise ValueError("height_page_ratio must be between 0 and 1")

        if width_page_ratio < 0 or width_page_ratio > 1:
            raise ValueError("width_page_ratio must be between 0 and 1")

        self.min_height = 80
        self.height_page_ratio = height_page_ratio
        self.width_page_ratio = width_page_ratio

        self.overlap = overlap
        
        self.title = Text_decorator(title)

        header = ft.Row(
            [
                self.title,
            ],
            alignment= ft.MainAxisAlignment.END,
            expand=True
        )

        self.invisi_container = ft.Container(
            height=80,
            bgcolor= ft.Colors.with_opacity(0, "black"),
            padding= 10,
            content= header,
            alignment= ft.alignment.top_right
        )

        self.outline = PokedexBottomShape(color=color, width_ratio = self.width_page_ratio)
        
        self.structure = ft.Stack([
            self.outline,
            self.invisi_container
        ],
        bottom= 0,
        alignment= ft.alignment.top_right
        )
        super().__init__(
            bgcolor= ft.Colors.with_opacity(0, "black"),
        )

    def _update_children(self, e = None):
        height = self.page.height * self.height_page_ratio

        height = height if height > self.min_height else self.min_height

        width = self.page.width

        self.outline.draw_zigzag(width= width, height= height + self.overlap)
        self.outline.update()
        self.invisi_container.width = width
        self.invisi_container.height = height
        self.invisi_container.update()
        self.update()


    def did_mount(self):
        #make sure the control is at the top of the page# Ensure this component appears last (at the bottom)
        if self in self.page.controls:
            self.page.controls.remove(self)
        self.page.controls.append(self)
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
        poke = BottomPokedex(height_page_ratio= 3/5)
        page.add (poke)
        page.add(ft.TextField(hint_text="insert_query", on_submit= lambda _ : poke.show_query_field("lol")))

    ft.app(target=main)