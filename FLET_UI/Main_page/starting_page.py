import flet as ft

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Custom_elements.text_decorator import Text_decorator
from FLET_UI.Main_page.lighting_button import lighting_button

class starting_page(ft.Container):
    def __init__(self):
        """
        The main_page is going to be a very siplified view of the pokedex with a simple textfield and description of the website functionalities
        """
        super().__init__(
            expand= True,
            bgcolor= "red",
            padding= 30,
        )

        self.light_buttons = ft.Row([
            lighting_button(50, "Blue", do_blink= True),
            lighting_button(25, "red"),
            lighting_button(25, "yellow"),
            lighting_button(25, "green"),
            ],
            expand_loose= True
            )
    
        self.title = Text_decorator("This is Pokemon Relational Graph", expand_loose= True)

        self.input_box = ft.TextField(
            hint_text= "Insert here your query",
            multiline= True,
            bgcolor= "grey",
            expand_loose= True,
            suffix= ft.IconButton(ft.Icons.SEND, on_click=self.send_query),
        )

        self.upper_view = ft.Column(
            [self.light_buttons, self.title, ft.Divider(opacity=0), self.input_box],
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            expand_loose=True
        )

        self.description_box = ft.Container(
            content= ft.Text("This is a test description", selectable= True),
            bgcolor= "grey",
            padding=10,
            margin=10,
            border_radius= 20,
            expand= True,
        )

        self.content = ft.Column([self.upper_view, self.description_box], expand= True, horizontal_alignment= ft.CrossAxisAlignment.STRETCH)

    def send_query(self, e:ft.ControlEvent):
        query = self.input_box.value
        print(query)

if __name__ == "__main__":
    def main(page: ft.Page):
        page.add(starting_page())

ft.app(target=main)

