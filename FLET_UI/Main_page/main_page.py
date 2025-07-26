import flet as ft

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Custom_elements.text_decorator import Text_decorator

class main_page(ft.Container):
    def __init__(self):
        """
        The main_page is going to be a very siplified view of the pokedex with a simple textfield and description of the website functionalities
        """
        super().__init__(
            expand= True,
            bgcolor= "red",
            padding= 30,
        )
    
        self.title = Text_decorator("This is Pokemon Relatonal Graph")

        self.input_box = ft.TextField(
            hint_text= "Insert here your query",
            multiline= True,
            bgcolor= "grey"
        )

        self.upper_view = ft.Column(
            [self.title, ft.Divider(opacity=0), self.input_box],
            expand=1, 
            horizontal_alignment= ft.CrossAxisAlignment.CENTER
        )

        self.description_box = ft.Container(
            content= ft.Text("This is a test description", selectable= True),
            bgcolor= "grey",
            padding=10,
            margin=10,
            border_radius= 20,
            expand= 3
        )

        self.content = ft.Column([self.upper_view, self.description_box], expand= True, horizontal_alignment= ft.CrossAxisAlignment.STRETCH)

if __name__ == "__main__":
    def main(page: ft.Page):
        page.add(main_page())

ft.app(target=main)

