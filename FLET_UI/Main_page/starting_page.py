import asyncio
from typing import Optional
import flet as ft

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Custom_elements.text_decorator import Text_decorator
from FLET_UI.Main_page.lighting_button import lighting_button
from FLET_UI.Main_page.Top_navigation_Pokedex import TopNavigationPokedex


class Starting_page(ft.Container):
    def __init__(self, on_submit_query: Optional[callable] = None):
        """
        The main_page is going to be a very siplified view of the pokedex with a simple textfield and description of the website functionalities
        """
        border = ft.Border(bottom= ft.BorderSide(10, "grey"))
        
        super().__init__(
            expand= True,
            offset= ft.Offset(0,0),
            animate_offset=ft.Animation(1000, ft.AnimationCurve.LINEAR),
            bgcolor= ft.Colors.RED_400,
            padding= 30,
            border_radius= 30,
            border= border,
        )

        self.on_submit_query :callable = on_submit_query
    
        self.title = Text_decorator("This is Pokemon Relational Graph", expand_loose= True)

        self.input_box = ft.TextField(
            hint_text= "Insert here your query",
            multiline= True,
            bgcolor= "grey",
            expand_loose= True,
            suffix= ft.IconButton(ft.Icons.SEND, on_click=self.send_query),
        )

        self.upper_view = ft.Column(
            [self.title, ft.Divider(opacity=0), self.input_box],
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

        self.content = ft.Column(
                [self.upper_view, self.description_box],
                expand= True,
                horizontal_alignment= ft.CrossAxisAlignment.STRETCH
            )

    def send_query(self, e:ft.ControlEvent):
        query = self.input_box.value
        e.control.data = query
        print(query)
        if self.on_submit_query:
            self.on_submit_query(e)

    def animate_out(self, on_animation_end : Optional[callable] = None):
        def at_end(e: ft.ControlEvent):
            self.visible = False
            if on_animation_end: on_animation_end(e)

        self.on_animation_end = at_end
        self.offset =  ft.Offset(0, -1.5)
        self.update()

    def animate_in(self, on_animation_end: Optional[callable] = None): 
        #not used       
        def at_end(e: ft.ControlEvent):
            if on_animation_end: on_animation_end(e)

        self.visible = True
        self.on_animation_end = at_end
        self.offset =  ft.Offset(0, -1.5)
        self.update()

    """
    def did_mount(self):
        self.offset = ft.Offset(0, -1.5)
        self.update()
        self.page.run_task(self._delayed_animate)
    """

    async def _delayed_animate(self):
        await asyncio.sleep(0.05)  # Delay lets initial state render
        self.offset = ft.Offset(0, 0)
        self.update()
        
if __name__ == "__main__":
    def main(page: ft.Page):
        start = None

        def proceed(e):
            nonlocal start
            page.remove(start)
            start = Starting_page(on_submit_query= animate)
            page.add(start)

        def animate(e):
            start.animate_out(on_animation_end= proceed)

        start = Starting_page(on_submit_query= animate)

        page.add(TopNavigationPokedex())
        page.add(start)

    ft.app(target=main)

