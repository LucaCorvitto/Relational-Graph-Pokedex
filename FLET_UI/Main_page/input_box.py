from typing import Optional
from flet import Colors, Container, ControlEvent, TextField, Margin, Padding, border, Stack, alignment
import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Main_page.Poke_button import PokeballButton

class PokeballInput(Container):
    def __init__(
            self,
            on_pokeball_click: Optional[callable] = None,
            on_submit: Optional[callable] = None,
            radius: int = 80,
            bgcolor: Colors | str = "white",
            on_change: Optional[callable] = None,
            hint_text: Optional[str] = None,
            value: Optional[str] = None
    ):
        super().__init__()
        self.radius = radius
        self.expand_loose = True

        self.button = PokeballButton(on_click=on_pokeball_click, radius=radius)

        def change(e: ControlEvent):
            if on_change:
                on_change(e)

        # Save TextField reference
        self.textfield = TextField(
            border="none",
            value=value,
            hint_text=hint_text,
            multiline=True,
            min_lines=1,
            max_lines=4,
            expand=True,
            on_submit=on_submit,
            on_change=change,
        )

        self.textfield_container = Container(
            margin=Margin(left=radius * 0.3, top=radius * 0.3, right=0, bottom=0),
            padding=Padding(left=radius * 0.8, top=radius * 0.2, right=10, bottom=10),
            expand=True,
            bgcolor=bgcolor,
            border_radius=10,
            border=border.all(1, "lightgray"),
            content=self.textfield,
        )

        self.content = Stack(
            expand=True,
            alignment=alignment.top_left,
            controls=[
                self.textfield_container,
                Container(
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
    from flet import Page, app
    def main(page: Page):
        def on_button_click(e):
            print("Button clicked!")
            
        def submit(e):
            print(f"submitted: {e.control.value}")

        page.padding = 30
        page.add(PokeballInput(on_pokeball_click=on_button_click, on_submit=submit, hint_text= "hint"))

    app(target=main)
