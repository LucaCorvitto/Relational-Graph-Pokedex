import asyncio
from typing import Optional
from flet import (
    Stack, Animation, AnimationCurve, Colors, Row, MainAxisAlignment, Container,
    alignment
)

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Custom_elements.text_decorator import Text_decorator
from FLET_UI.Main_page.Poke_shape import PokedexShape

class BottomPokedex(Stack):
    """
    Make sure to append this on the page overlay.
    """
    INTRINSIC_OFFSET = 13
    def  __init__(
            self,
            title: Optional[str] = "Pokedex",
            color : Optional[Colors] = "red",
            height_page_ratio : float = 1/8,
            width_page_ratio : float = 1/2,
        ):

        self.previous_handler = None #used in did_mount
        
        if height_page_ratio < 0 or height_page_ratio > 1:
            raise ValueError("height_page_ratio must be between 0 and 1")

        if width_page_ratio < 0 or width_page_ratio > 1:
            raise ValueError("width_page_ratio must be between 0 and 1")

        self.min_height = 80
        self.height_page_ratio = height_page_ratio
        self.width_page_ratio = width_page_ratio
        
        self.title = Text_decorator(title)

        header = Row(
            [
                self.title,
            ],
            alignment= MainAxisAlignment.END,
            expand=True
        )

        self.invisi_container = Container(
            height=80,
            bgcolor= Colors.with_opacity(0, "black"),
            padding= 10,
            content= header,
            alignment= alignment.bottom_right
        )

        self.outline = PokedexShape(color=color, width_ratio = self.width_page_ratio, flipped= True)
        
        super().__init__([
            self.outline,
            self.invisi_container
        ],
        bottom= BottomPokedex.INTRINSIC_OFFSET,
        alignment= alignment.top_right,
        animate_position = Animation(500, AnimationCurve.LINEAR),
        )

        self._is_open = False  # ← Track open state

    def _update_children(self, e=None):
        height = self.page.height * self.height_page_ratio
        height = max(height, self.min_height)
        width = self.page.width

        self.outline.draw_zigzag(width=width, height=height)
        self.outline.update()
        self.invisi_container.width = width
        self.invisi_container.height = height
        self.invisi_container.update()

        # ⬇ Reapply open/close position based on state after resizing
        if self._is_open:
            self.bottom = -(height / 2) + BottomPokedex.INTRINSIC_OFFSET
        else:
            self.bottom = BottomPokedex.INTRINSIC_OFFSET

        self.update()

    def open(self):
        """
        Slide the element upward by half its height (off-screen).
        """
        self.animate_position = Animation(400, AnimationCurve.EASE_OUT)
        height = self.page.height * self.height_page_ratio
        height = max(height, self.min_height)

        self.bottom = -(height / 2) + BottomPokedex.INTRINSIC_OFFSET
        self._is_open = True
        self.update()

    def close(self):
        """
        Return to the default resting position.
        """
        self.animate_position = Animation(400, AnimationCurve.EASE_OUT)
        self.bottom = BottomPokedex.INTRINSIC_OFFSET
        self._is_open = False
        self.update()

    def toggle_open_close(self):
        """
        Toggles between open and close states.
        """
        if self._is_open:
            self.close()
        else:
            self.open()



    def did_mount(self):
        self._update_children()

        # Chain on_resized handlers
        if getattr(self, "_handler_attached", False):
            return
        self._previous_handler = self.page.on_resized
        self._handler_attached : bool = False
        def combined_handler(e):
            self._update_children(e)
            if self._previous_handler:
                self._previous_handler(e)

        self.page.on_resized = combined_handler
        self._handler_attached = True
        
    def _animate_scrolling(self, target_position: int):
        """
        Target position is relative to the page
        if you wish to call this animation, write another code that calls for self.on_animation_end at the end of the animation
        (it has to be a different function to avoid conflicts with animate_open_close)
        """
        target_position = target_position + BottomPokedex.INTRINSIC_OFFSET
        self.bottom = target_position
        self.update()

    def animate_open_close(
            self,
            target_position: float = 0.3,
            delay_ms: int = 500,
            on_half_animation : Optional[callable] = None
        ):
        """
        Moves structure to `target_position`, waits for `delay_ms`,
        then animates back to 0.
        """
        # Ensure animate_position is set
        self.animate_position = Animation(500, AnimationCurve.EASE_IN_OUT)

        async def delayed_return(_):
            if on_half_animation:
                on_half_animation(_)
            # Wait for given milliseconds
            await asyncio.sleep(delay_ms / 1000)
            if self.on_animation_end:
                self.on_animation_end = self.on_animation_end
            self._animate_scrolling(0)

        # Attach async callback
        self.on_animation_end = lambda e: self.page.run_task(delayed_return, e)

        # Start animation
        self._animate_scrolling(self.page.height * target_position)

if __name__ == "__main__":
    from flet import Page, IconButton, Icons, app
    def main(page: Page):
        poke = BottomPokedex()
        page.add(IconButton(Icons.ABC, on_click= lambda _: poke.toggle_open_close()))
        page.overlay.append(poke)
        page.update()

    app(target=main)