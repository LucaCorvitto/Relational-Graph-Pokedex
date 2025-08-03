import asyncio
import time
from typing import Optional
import flet as ft
import flet.canvas as cv

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Custom_elements.text_decorator import Text_decorator
from FLET_UI.Custom_elements.lighten_color import lighten_color
from FLET_UI.Main_page.lighting_button import lighting_button
from FLET_UI.Main_page.Pokedex_screen import Pokedex_screen

#POKEDEX SHAPE------------------------------------------------------
class PokedexTopShape(cv.Canvas):
    def __init__(
            self,
            color: ft.Colors = "blue",
            width_ratio : float = 1/2,
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
            cv.Path.LineTo(self.width, -self.height/2 + y_offset) if y_offset else cv.Path.LineTo(self.width, -self.height*5),
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
                    stroke_width=8,
                    style=ft.PaintingStyle.STROKE,
                    color=ft.Colors.BLACK38,
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
        shadow_path = [cv.Path.MoveTo(0, self.height *9/10 + self.shadow_offset)]
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
            width_page_ratio : float = 1/2,
            overlap : int = 25,
            on_submit_query : Optional[callable] = None,
            on_expand_query : Optional[callable] = None,
            expanded_view : bool = True
        ):
        
        if height_page_ratio < 0 or height_page_ratio > 1:
            raise ValueError("height_page_ratio must be between 0 and 1")
        
        if width_page_ratio < 0 or width_page_ratio > 1:
            raise ValueError("width_page_ratio must be between 0 and 1")

        self.min_height = 350 if expanded_view else 80
        self.height_page_ratio = height_page_ratio
        self.width_page_ratio = width_page_ratio

        self._vibrating = None

        self.overlap = overlap

        self.expanded_view = expanded_view
        self.color = color
        self.on_submit_query = on_submit_query

        self.light_0 = lighting_button(50, "Blue", do_blink= True)
        self.light_1 = lighting_button(25, "red")
        self.light_2 = lighting_button(25, "orange")
        self.light_3 = lighting_button(25, "green")

        self.light_buttons = ft.Row( [
            ft.Divider(),
            self.light_0,
            self.light_1,
            self.light_2,
            self.light_3
            ], spacing= 3)
        
        self.title = Text_decorator(title)

        self.query_field_prefix = ft.IconButton(ft.Icons.EXPAND, on_click= on_expand_query, visible=False)

        self.query_field = Pokedex_screen(
            on_submit= self.on_submit_query,
            prefix= self.query_field_prefix,
            height= 70,
            on_change= self.sync_queries,
        )
        
        self.invisi_divider = ft.VerticalDivider(width= 70, opacity= 0)
        self.header = ft.Row(
            [
                self.light_buttons,
                self.invisi_divider,
                self.query_field
            ],
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment= ft.CrossAxisAlignment.END,
        )
        
        self.input_box = ft.Divider(visible=False)
        self.description_box = ft.Divider(visible=False)

        if self.expanded_view:
            self.create_expanded_body()

        self.upper_view = ft.Container(
            ft.Column(
                [self.title, self.input_box, self.description_box],
                horizontal_alignment= ft.CrossAxisAlignment.CENTER
                ),
            expand = True,
            padding= 20,
            visible= self.expanded_view
        )

        spacer = ft.Divider(height= self.overlap/2, opacity=0)

        content_column = ft.Column(
            controls=[
                self.upper_view,
                self.header,
                spacer
            ],
            alignment= ft.MainAxisAlignment.END
        )

        self.invisi_container = ft.Container(
            height=80,
            bgcolor= ft.Colors.with_opacity(0, "black"),
            padding= 10,
            content= content_column,
            alignment= ft.alignment.bottom_center
        )

        self.outline = PokedexTopShape(color=color, width_ratio = width_page_ratio)
        
        self._default_animation = ft.Animation(500, ft.AnimationCurve.EASE)
        self.structure = ft.Stack([
            self.outline,
            self.invisi_container
        ],
        animate_position = self._default_animation,
        top= 0
        )

        super().__init__(
            content= ft.Text("This is TopNavigationPokedex placeholder"),
        )

    def create_expanded_body(self):
        self.input_box = ft.TextField(
            hint_text= "Insert here your query",
            multiline= True,
            bgcolor= lighten_color(self.color),
            expand_loose= True,
            suffix= ft.IconButton(ft.Icons.SEND, on_click= self.on_submit_query),
            max_lines= 4,
            on_change= self.sync_queries,
        )

        self.description_box = ft.Container(
            content= ft.Text("This is a test description", selectable= True),
            bgcolor= lighten_color(self.color),
            padding=10,
            margin=10,
            border_radius= 20,
            expand_loose= True,
        )

    def sync_queries(self, e):
        if e.control == self.query_field.text_screen:
            self.input_box.value = self.query_field.text_screen.value
            self.input_box.update()
        else:
            self.query_field.text_screen.value = self.input_box.value
            self.query_field.text_screen.update()

    def show_hide_expand_query(self):
        self.query_field_prefix.visible = not self.query_field_prefix.visible

    def show_query_field(self, query: Optional[str] = None):
        self.query_field.text_screen.value = query
        self.query_field.visible = True
        self.query_field.update()
    
    def hide_query_field(self):
        self.query_field.visible = False
        self.query_field.update()

    def rescale_light_buttons(self, scale):
        for button in self.light_buttons.controls:
            if button.__class__ == lighting_button:
                button.radius = button.radius * scale
                button.update()
        self.light_buttons.spacing = self.light_buttons.spacing* scale

    def _reduce_scale(self):
        """
        reduces the scale of the buttons and other UI elements to improve UI responsiveness
        """
        
        if getattr(self, "_scale_reduced", False):
            return
        
        self.rescale_light_buttons(0.8)
        self.upper_view.padding = 10
        self.upper_view.update()
        self.invisi_divider.visible = False
        self.invisi_divider.update()
        self._scale_reduced = True

    def _restore_scale(self):
        """
        restores the scale at normal if the page allows
        """
        if not getattr(self, "_scale_reduced", False):
            return
        
        self.rescale_light_buttons(1.25)
        self.upper_view.padding = 20
        self.upper_view.update()
        self.invisi_divider.visible = True
        self.invisi_divider.update()
        self._scale_reduced = False

    def _update_children(self, e = None):
        height = self.page.height * self.height_page_ratio

        height = height if height > self.min_height else self.min_height

        self.width = self.page.width

        #reduce size of buttons if page width is small (responsive UI)
        if self.width <350:
            self._reduce_scale()
        else:
            self._restore_scale()

        self.height = height - self.overlap
        self.outline.draw_zigzag(width= self.width, height= height)
        self.outline.update()
        self.invisi_container.height = height
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
        if getattr(self, "_handler_attached", False):
            return
        self._previous_handler = self.page.on_resized
        def combined_handler(e):
            self._update_children(e)
            if self._previous_handler:
                self._previous_handler(e)

        self.page.on_resized = combined_handler
        self._handler_attached = True

    def will_unmount(self):
        self.stop_vibrate()
        if self._previous_handler:
            self.page.on_resized = self._previous_handler
        self.page.overlay.remove(self.structure)
        self.page.update()

    def _animate_scrolling(self, target_position: int):
        self.structure.top = target_position
        self.structure.update()
            
    async def _vibrate_process(self, amplitude: float = 0.7, frequency: float = 0.05):
        """
        Simulates vibration by oscillating around the initial top position.
        `amplitude`: pixel displacement up/down.
        `frequency`: time in seconds between oscillations.
        """
        self.structure.animate_position = ft.Animation(50, ft.AnimationCurve.LINEAR)

        direction = 1
        while True:
            self.structure.top = direction * amplitude
            self.structure.update()
            direction *= -1
            await asyncio.sleep(frequency)

    
    def start_vibrate(self):
        self._vibrating = self.page.run_task(self._vibrate_process)

    def stop_vibrate(self):
        if self._vibrating:
            self._vibrating.cancel()
            self.structure.top = 0
            self.structure.update()
            self._vibrating = None

    def animate_open_close(
            self,
            target_position: float = 0.4,
            delay_ms: int = 500,
            on_half_animation : Optional[callable] = None
        ):
        """
        target position is proportional to page
        Moves structure to `target_position`, waits for `delay_ms`,
        then animates back to 0.
        """

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
        target_position = target_position * self.page.height
        self._animate_scrolling(target_position)

    def processing_query_animation(self):
        """
        Lights up buttons, shows processing.
        """
        self.start_vibrate()
        self.light_0.stop_blinking()
        self.light_0.start_blinking(frequency= 0.25)
        time.sleep(0.15)
        self.light_1.start_blinking(frequency= 0.5)
        time.sleep(0.15)
        self.light_2.start_blinking(frequency= 0.5)
        time.sleep(0.15)
        self.light_3.start_blinking(frequency= 0.5)

if __name__ == "__main__":
    def main(page: ft.Page):

        # This triggers after did_mount has placed structure in overlay
        def move(e):
            poke.on_animation_end = lambda _: print("finito!")
            poke.animate_open_close(0.5, on_half_animation= lambda _: print("siamo a meta'!"))

        poke = TopNavigationPokedex(on_submit_query= move)

        page.add(ft.TextField(
            hint_text="insert_query",
            on_submit=move
        ))

        page.add(poke)

    ft.app(target=main)