from typing import Optional
from flet import (
    Container, Rotate, alignment, Animation, AnimationCurve,
    BoxShadow, Offset, border_radius, Stack
    )
import math
import asyncio

class PokeballButton(Container):
    def __init__(self, on_click : Optional[callable] = None, radius: int = 100):
        super().__init__()
        self.radius = radius
        self.on_click_callback = on_click
        self.angle = -math.pi/4
        self.task = None  # Used to control async rotation
        self._rotating = False

        self.pokeball = Container(  # Inner rotating container
            rotate=Rotate(angle=self.angle),
            animate_rotation=Animation(500, AnimationCurve.SLOW_MIDDLE),
            content=self._build_pokeball(),
            width=self.radius,
            height=self.radius,
            alignment=alignment.center,
        )

        self.content = self.pokeball  # Set outer content to the inner rotator
        self.width = radius
        self.height = radius
        self.bgcolor = "green"
        self.border_radius = radius
        self.alignment = alignment.center
        self.shadow = BoxShadow(spread_radius=2, blur_radius=2, offset=Offset(2, 4))
        self.on_click = self._on_click  # Hook internal method

    def _build_pokeball(self):
        r = self.radius
        return Stack(
            width=r,
            height=r,
            alignment=alignment.center,
            controls=[
                # Bottom half
                Container(
                    top=r / 2,
                    width=r,
                    height=r / 2,
                    bgcolor="white",
                    border_radius=border_radius.only(bottom_left=r / 2, bottom_right=r / 2),
                ),
                # Top half
                Container(
                    top=0,
                    width=r,
                    height=r / 2,
                    bgcolor="red",
                    shadow=BoxShadow(spread_radius=r / 20),
                    border_radius=border_radius.only(top_left=r / 2, top_right=r / 2),
                ),
                # Center circle
                Container(
                    alignment=alignment.center,
                    width=r * 0.35,
                    height=r * 0.35,
                    bgcolor="black",
                    border_radius=r * 0.2,
                    content=Container(
                        width=r * 0.2,
                        height=r * 0.2,
                        bgcolor="white",
                        border_radius=r * 0.1,
                    )
                )
            ]
        )
    
    async def _on_click(self, e):
        self.start_rotating()

        # Handle both sync and async callbacks
        if self.on_click_callback:
            result = self.on_click_callback(e)
            if asyncio.iscoroutine(result):
                # Wait for BOTH: callback AND at least 2 seconds
                await asyncio.gather(result, asyncio.sleep(2))
            else:
                # Sync call: still ensure 2-second wait
                await asyncio.sleep(2)
        else:
            await asyncio.sleep(2)

        self.stop_rotating()

    async def _rotate(self):
        self.task = asyncio.current_task()
        while self._rotating:
            self.angle += 2 * math.pi
            self.pokeball.rotate = self.angle
            self.pokeball.update()
            await asyncio.sleep(1)

    def start_rotating(self):
        if self._rotating:
            return
        self._rotating = True
        self.page.run_task(self._rotate)

    def stop_rotating(self):
        if self._rotating:
            self._rotating = False
            self.task.cancel()
            self.task = None

if __name__ == "__main__":
    from flet import Page, app, MainAxisAlignment, CrossAxisAlignment
    def main(page: Page):
        page.window.height = 300
        page.window.width = 300
        page.title = "Pokéball Button"
        page.vertical_alignment = MainAxisAlignment.CENTER
        page.horizontal_alignment = CrossAxisAlignment.CENTER

        async def on_button_click(e):
            print("Pokéball clicked!")
            await asyncio.sleep(5)

        page.add(PokeballButton(radius=50, on_click=on_button_click))

    app(target=main)
