import asyncio
import time
from typing import Optional
from flet import (
    Container, Colors, Row, Column, Stack, Divider, IconButton, Icons, Divider, VerticalDivider,
    MainAxisAlignment, CrossAxisAlignment, Animation, AnimationCurve, alignment, Text
)
import flet as ft

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Custom_elements.text_decorator import Text_decorator
from FLET_UI.Custom_elements.lighten_color import lighten_color
from FLET_UI.Main_page.lighting_button import lighting_button
from FLET_UI.Main_page.Pokedex_screen import Pokedex_screen
from FLET_UI.Main_page.input_box import PokeballInput
from FLET_UI.Main_page.Poke_shape import PokedexShape

class TopNavigationPokedex(Container):
    MIN_HEIGHT_HIDE_BODY = 80
    MIN_HEIGHT_SHOW_BODY = 350

    def  __init__(
            self,
            title: Optional[str] = "Pokedex",
            color : Optional[Colors] = "red",
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

        self.min_height = TopNavigationPokedex.MIN_HEIGHT_SHOW_BODY if expanded_view else TopNavigationPokedex.MIN_HEIGHT_HIDE_BODY
        self.height_page_ratio = height_page_ratio
        self.width_page_ratio = width_page_ratio

        self._vibrating = None
        self.processing = False

        self.overlap = overlap

        self.expanded_view = expanded_view
        self.color = color
        self.on_submit_query = on_submit_query

        self.light_0 = lighting_button(50, "Blue", do_blink= True)
        self.light_1 = lighting_button(25, "red")
        self.light_2 = lighting_button(25, "orange")
        self.light_3 = lighting_button(25, "green")

        self.light_buttons = Row( [
            Divider(),
            self.light_0,
            self.light_1,
            self.light_2,
            self.light_3
            ], spacing= 3)
        
        self.title = Text_decorator(title)

        self.query_field_prefix = IconButton(Icons.EXPAND, on_click= on_expand_query, visible=False, icon_color= "green")

        self.query_field = Pokedex_screen(
            on_submit= self.on_submit_query,
            prefix= self.query_field_prefix,
            height= 60,
            on_change= self._sync_queries,
        )
        
        self.invisi_divider = VerticalDivider(width= 70, opacity= 0)
        self.header = Row(
            [
                self.light_buttons,
                self.invisi_divider,
                self.query_field
            ],
            alignment= MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment= CrossAxisAlignment.END,
        )
        
        self.create_expanded_body()

        spacer = Divider(height= self.overlap/2, opacity=0)

        content_column = Column(
            controls=[
                self.expanded_body,
                self.header,
                spacer
            ],
            alignment= MainAxisAlignment.END
        )

        self.invisi_container = Container(
            height=TopNavigationPokedex.MIN_HEIGHT_HIDE_BODY,
            bgcolor= Colors.with_opacity(0, "black"),
            padding= 10,
            content= content_column,
            alignment= alignment.bottom_center
        )

        self.outline = PokedexShape(color=color, width_ratio = width_page_ratio)
        
        self._default_animation = Animation(500, AnimationCurve.EASE)
        self.structure = Stack([
            self.outline,
            self.invisi_container
        ],
        animate_position = self._default_animation,
        top= 0
        )

        super().__init__(
            content= Text("This is TopNavigationPokedex placeholder"),
        )

    def create_expanded_body(self):
        self.input_box = PokeballInput(
            hint_text= "Insert here your query",
            bgcolor= lighten_color(self.color),
            on_submit= self.on_submit_query,
            on_change= self._sync_queries,
        )

        self.description_box = Container(
            content= Text("This is a test description", selectable= True),
            bgcolor= lighten_color(self.color),
            padding=10,
            margin=10,
            border_radius= 20,
            expand_loose= True,
        )

        self.expanded_body = Container(
            Column(
                [self.title, self.input_box, self.description_box],
                horizontal_alignment= CrossAxisAlignment.CENTER
                ),
            expand = True,
            padding= 20,
            visible= self.expanded_view
        )

    def _sync_queries(self, e):
        if e.control == self.query_field.text_screen:
            self.input_box.value = self.query_field.text_screen.value
            self.input_box.update()
        else:
            self.query_field.text_screen.value = self.input_box.value
            self.query_field.text_screen.update()

    def set_query(self, query):
        self.input_box.value = query
        self.query_field.text_screen.value = query
        self.input_box.update()
        self.query_field.text_screen.update()

    def show_expand_icon(self):
        self.query_field_prefix.visible = True
        self.query_field.update()

    def hide_expand_icon(self):
        self.query_field_prefix.visible = False
        self.query_field.update()

    def toggle_expand_icon(self):
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
        self.expanded_body.padding = 10
        self.expanded_body.update()
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
        self.expanded_body.padding = 20
        self.expanded_body.update()
        self.invisi_divider.visible = True
        self.invisi_divider.update()
        self._scale_reduced = False

    def _update_children(self, e=None):
        if not self.page:
            return

        if self.expanded_view:
            height = self.page.height * self.height_page_ratio
            height = max(height, self.min_height)
        else:
            height = TopNavigationPokedex.MIN_HEIGHT_HIDE_BODY + self.overlap

        self.width = self.page.width
        self.height = height - self.overlap

        # Reduce button size on small screens (responsive UI)
        if self.width < 350:
            self._reduce_scale()
        else:
            self._restore_scale()

        # Redraw shape
        self.outline.draw_zigzag(width=self.width, height=height)
        self.outline.update()

        # Update the invisible container dimensions
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
        self.structure.animate_offset = self._default_animation
        self.structure.top = target_position
        self.structure.update()
            
    async def _vibrate_process(self, amplitude: float = 0.7, frequency: float = 0.05):
        """
        Simulates vibration by oscillating around the initial top position.
        `amplitude`: pixel displacement up/down.
        `frequency`: time in seconds between oscillations.
        """
        self.structure.animate_position = Animation(50, AnimationCurve.LINEAR)

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

    def hide_body(self):
        if not self.expanded_view:
            return
        
        def hide_upper_view(e):
            if self.on_animation_end:
                self.structure.on_animation_end = self.on_animation_end
            self.expanded_body.visible = False
            self.expanded_body.update()
            self._animate_scrolling(0)
            self._update_children()

        self.expanded_view = False
        self.min_height = TopNavigationPokedex.MIN_HEIGHT_HIDE_BODY
        target_position = -(self.height) + self.min_height
        self.structure.on_animation_end = hide_upper_view
        self._animate_scrolling(target_position)
        
    def show_body(self):
        if self.expanded_view:
            return
        
        def on_end(_):
            if self.on_animation_end:
                self.structure.on_animation_end = self.on_animation_end
            self._animate_scrolling(0)

        self.expanded_body.visible = True
        self.expanded_body.update()
        self.expanded_view = True
        self.min_height = TopNavigationPokedex.MIN_HEIGHT_SHOW_BODY
        self._update_children()
        self.structure.on_animation_end = on_end
        self._animate_scrolling(self.min_height/5)


    def start_processing_query_animation(self, loading_text : str = "Loading..."):
        """
        Lights up buttons, shows processing.
        """
        if self.processing:
            return
        self.processing = True
        if isinstance(self.input_box , PokeballInput):
            self.input_box.button.start_rotating()
        self.query_field.start_loading(loading_text)
        self.light_0.stop_blinking()
        self.light_0.start_blinking(frequency= 0.25)
        time.sleep(0.15)
        self.light_1.start_blinking(frequency= 0.5)
        time.sleep(0.15)
        self.light_2.start_blinking(frequency= 0.5)
        time.sleep(0.15)
        self.light_3.start_blinking(frequency= 0.5)

    def stop_processing_query_animation(self):
        if not self.processing:
            return
        self.processing = False
        if isinstance(self.input_box , PokeballInput):
            self.input_box.button.stop_rotating()
        self.query_field.stop_loading()
        self.light_0.stop_blinking()
        self.light_0.start_blinking()
        self.light_1.stop_blinking()
        self.light_2.stop_blinking()
        self.light_3.stop_blinking()
        

if __name__ == "__main__":
    from flet import Page, TextField, app
    def main(page: Page):

        def move(e):
            if poke.expanded_view == False:
                poke.show_body()
            else:
                poke.hide_body()

        poke = TopNavigationPokedex(on_submit_query= move, expanded_view= False)

        page.add(TextField(
            hint_text="insert_query",
            on_submit=move
        ))

        page.add(poke)

    app(target=main)