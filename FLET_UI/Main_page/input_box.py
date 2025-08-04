from typing import Optional
import flet as ft
import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Main_page.Poke_button import PokeballButton

class PokeballInput(ft.Container):
    def __init__(
            self,
            on_pokeball_click: Optional[callable] = None,
            on_submit: Optional[callable] = None,
            radius: int = 80,
            bgcolor: ft.Colors | str = "white",
            on_change: Optional[callable] = None,
            hint_text: Optional[str] = None,
            value: Optional[str] = None
    ):
        super().__init__()
        self.radius = radius
        self.expand_loose = True

        self.button = PokeballButton(on_click=on_pokeball_click, radius=radius)

        def change(e: ft.ControlEvent):
            if on_change:
                on_change(e)

        # Save TextField reference
        self.textfield = ft.TextField(
            border="none",
            value=value,
            hint_text=hint_text,
            multiline=True,
            min_lines=1,
            max_lines=4,
            expand=True,
            on_submit=on_submit,
            shift_enter=True,
            on_change=change,
        )

        self.textfield_container = ft.Container(
            margin=ft.Margin(left=radius * 0.3, top=radius * 0.3, right=0, bottom=0),
            padding=ft.Padding(left=radius * 0.8, top=radius * 0.2, right=10, bottom=10),
            expand=True,
            bgcolor=bgcolor,
            border_radius=10,
            border=ft.border.all(1, "lightgray"),
            content=self.textfield,
        )

        self.content = ft.Stack(
            expand=True,
            alignment=ft.alignment.top_left,
            controls=[
                self.textfield_container,
                ft.Container(
                    left=0,
                    top=0,
                    content=self.button,
                    width=radius,
                    height=radius,
                )
            ],
        )

    # Passthrough: value
    @property
    def value(self):
        return self.textfield.value

    @value.setter
    def value(self, new_value):
        self.textfield.value = new_value
            
    def update(self):
        super().update()
        self.textfield.update()

    def focus(self):
        self.textfield.focus()

    def clear(self):
        self.textfield.value = ""
        self.textfield.update()


if __name__ == "__main__":
    def main(page: ft.Page):
        def on_button_click(e):
            print("Button clicked!")
            
        def submit(e):
            print(f"submitted: {e.control.value}")

        page.padding = 30
        page.add(PokeballInput(on_pokeball_click=on_button_click, on_submit=submit, hint_text= "hint"))

    ft.app(target=main)
