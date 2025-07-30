import asyncio
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
    def __init__(
            self,
            color: ft.Colors = "blue",
            width_ratio : float = 1/3,
            width = 80,
            heigth = 80,
            shadow_offset: float = 5.0,
            width_limit = 170
        ):
        super().__init__(expand=True)
        
        if width_ratio < 0 or width_ratio > 1:
            raise ValueError("width_ratio must be between 0 and 1")
        self.shadow_offset = shadow_offset
        self.color = color
        self.heigth = heigth
        self.width = width
        self.width_ratio = width_ratio

        #this limit is needed to keep the space for the lights.
        #set it to 0 to turn it off.
        self.width_limit = width_limit

    def draw_path(self, y_offset=0):

        if self.width_limit >0:
            width = self.width * self.width_ratio if self.width * self.width_ratio > self.width_limit else self.width_limit

        return [
            cv.Path.LineTo(0, self.height + y_offset),
            cv.Path.LineTo(width, self.height + y_offset),
            cv.Path.LineTo((width) +30, self.height -20 + y_offset),
            cv.Path.LineTo(self.width, self.height -20 + y_offset),
            cv.Path.LineTo(self.width, -self.height*5 + y_offset),
            cv.Path.Close(),
        ]

    def draw_zigzag(self, width, height, e=None):
        self.shapes = []

        self.width = width
        self.height = height

        # Main shape
        path_commands = [cv.Path.MoveTo(0, -self.height*5)]
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
            height_page_ratio : float = 1/8,
            width_page_ratio : float = 1/3,
            overlap : int = 25,
            on_submit_query : Optional[callable] = None,
            on_expand_query : Optional[callable] = None
        ):
        
        self.previous_handler = None # used in did_mount

        if height_page_ratio < 0 or height_page_ratio > 1:
            raise ValueError("height_page_ratio must be between 0 and 1")
        
        if width_page_ratio < 0 or width_page_ratio > 1:
            raise ValueError("width_page_ratio must be between 0 and 1")

        self.min_height = 80
        self.height_page_ratio = height_page_ratio
        self.width_page_ratio = width_page_ratio

        self.overlap = overlap

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

        self.outline = PokedexTopShape(color=color, width_ratio = width_page_ratio)
        
        self.structure = ft.Stack([
            self.outline,
            self.invisi_container
        ],
        animate_position = ft.Animation(500, ft.AnimationCurve.LINEAR),
        top= 0
        )

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
        self.outline.draw_zigzag(width= self.width, height= self.height + self.overlap)
        self.outline.update()
        self.invisi_container.height = self.height
        self.invisi_container.width = self.width
        self.invisi_container.update()
        self.update()


    def did_mount(self):
        #make sure the control is at the top of the page
        if self in self.page.controls:
            self.page.controls.remove(self)
        self.page.controls.insert(0, self)
        self.page.overlay.append(self.structure)
        self.page.update()
        self._update_children()
        # Chain on_resized handlers
        self.previous_handler = self.page.on_resized

        def combined_handler(e):
            self._update_children(e)
            if self.previous_handler:
                self.previous_handler(e)

        self.page.on_resized = combined_handler

    def will_unmount(self):
        if self.previous_handler:
            self.page.on_resized = self.previous_handler
        self.page.overlay.remove(self.structure)
        self.page.update()

    def _animate_scrolling(self, target_position: float):
        """
        Target position is relative to the page
        if you wish to call this animation, write another code that calls for self.on_animation_end at the end of the animation
        (it has to be a different function to avoid conflicts with animate_open_close)
        """
        target_position = self.page.height * target_position
        self.structure.top = target_position
        self.structure.update()

    def animate_open_close(
            self,
            target_position: float = 0.4,
            delay_ms: int = 500,
            on_half_animation : Optional[callable] = None
        ):
        """
        Moves structure to `target_position`, waits for `delay_ms`,
        then animates back to 0.
        """

        # Ensure animate_position is set
        self.structure.animate_position = ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)

        async def delayed_return(_):
            if on_half_animation:
                on_half_animation(_)
            # Wait for given milliseconds
            await asyncio.sleep(delay_ms / 1000)
            if self.on_animation_end:
                self.structure.on_animation_end = self.on_animation_end
            self._animate_scrolling(0)

        # Attach async callback
        self.structure.on_animation_end = lambda e: self.page.run_task(delayed_return, e)

        # Start animation
        self._animate_scrolling(target_position)


if __name__ == "__main__":
    def main(page: ft.Page):

        # This triggers after did_mount has placed structure in overlay
        def move(e):
            poke.show_query_field("lol")
            poke.on_animation_end = lambda _: print("finito!")
            poke.animate_open_close(0.5, on_half_animation= lambda _: print("siamo a meta'!"))

        poke = TopNavigationPokedex(on_submit_query= move)

        page.add(ft.TextField(
            hint_text="insert_query",
            on_submit=move
        ))

        page.add(poke)

    ft.app(target=main)