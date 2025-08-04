from typing import Optional
import flet as ft
import math
import asyncio

class PokeballButton(ft.Container):
    def __init__(self, on_click : Optional[callable] = None, radius: int = 100):
        super().__init__()
        self.radius = radius
        self.on_click_callback = on_click
        self.angle = -math.pi/4
        self.task = None  # Used to control async rotation

        self.pokeball = ft.Container(  # Inner rotating container
            rotate=ft.Rotate(angle=self.angle),
            animate_rotation=ft.Animation(500, ft.AnimationCurve.SLOW_MIDDLE),
            content=self._build_pokeball(),
            width=self.radius,
            height=self.radius,
            alignment=ft.alignment.center,
        )

        self.content = self.pokeball  # Set outer content to the inner rotator
        self.width = radius
        self.height = radius
        self.bgcolor = "green"
        self.border_radius = radius
        self.alignment = ft.alignment.center
        self.shadow = ft.BoxShadow(spread_radius=2, blur_radius=2, offset=ft.Offset(2, 4))
        self.on_click = self._on_click  # Hook internal method

    def _build_pokeball(self):
        r = self.radius
        return ft.Stack(
            width=r,
            height=r,
            alignment=ft.alignment.center,
            controls=[
                # Bottom half
                ft.Container(
                    top=r / 2,
                    width=r,
                    height=r / 2,
                    bgcolor="white",
                    border_radius=ft.border_radius.only(bottom_left=r / 2, bottom_right=r / 2),
                ),
                # Top half
                ft.Container(
                    top=0,
                    width=r,
                    height=r / 2,
                    bgcolor="red",
                    shadow=ft.BoxShadow(spread_radius=r / 20),
                    border_radius=ft.border_radius.only(top_left=r / 2, top_right=r / 2),
                ),
                # Center circle
                ft.Container(
                    alignment=ft.alignment.center,
                    width=r * 0.35,
                    height=r * 0.35,
                    bgcolor="black",
                    border_radius=r * 0.2,
                    content=ft.Container(
                        width=r * 0.2,
                        height=r * 0.2,
                        bgcolor="white",
                        border_radius=r * 0.1,
                    )
                )
            ]
        )

    def _on_click(self, e):
        if self.on_click_callback:
            self.on_click_callback(e)

        if self.task:
            self._stop_rotating()
        self.page.run_task(self._start_rotating)

    async def _start_rotating(self):
        self.task = asyncio.current_task()
        for _ in range(3):  # 3 seconds
            self.angle += 2 * math.pi
            self.pokeball.rotate = self.angle
            self.pokeball.update()
            await asyncio.sleep(1)
        self._stop_rotating()

    def _stop_rotating(self):
        if self.task:
            self.task.cancel()
            self.task = None

if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Pokéball Button"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def on_button_click(e):
            print("Pokéball clicked!")

        page.add(PokeballButton(radius=50, on_click=on_button_click))

    ft.app(target=main)
