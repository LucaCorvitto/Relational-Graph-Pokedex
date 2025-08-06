import flet as ft

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Main_page.Top_navigation_Pokedex import TopNavigationPokedex

class Main_structure(ft.Container):
    def __init__(self, query, response):
        super().__init__(expand=True)

        if "Errore" in response or "Error" in response:
            style = ft.TextStyle(size= 20, weight="bold", color= "orange")
        else:
            style = ft.TextStyle(color= "black")


        title = ft.TextStyle(size= 25, weight="bold")

        content = ft.Column([
            ft.Divider(height= 60),
            ft.Text("Current query =", style = title),
            ft.Text(f"<{query}>", style=style),
            ft.Text("LLM response =", style = title),
            ft.Text(f"<{response}>", style=style),
            ],
        expand=True
        )

        self.content = ft.Column([
            ft.Row([
                ft.Column(
                    [
                        ft.Container(width= 120, height=180, bgcolor="red"),
                        ft.Container(width=120, height=180, bgcolor="red"),
                        ft.Container(width=120, height=180, bgcolor="red"),
                        ft.Container(width=120, height=180, bgcolor="red")
                    ],
                    scroll= "always",
                    expand_loose= True
                ),
                ft.Divider(),
                ft.Container(bgcolor= "blue", expand= True, content= content)
                ],
                expand=True,
                vertical_alignment= ft.CrossAxisAlignment.START,
            )],
            spacing=0
            )
        
if __name__ == "__main__":
    def main(page: ft.Page):
        page.add(TopNavigationPokedex(height_page_ratio=2/5, expanded_view=False))
        page.add(Main_structure(query= "hello", response="Hello to you!"))

        page.update()

    ft.app(target=main)