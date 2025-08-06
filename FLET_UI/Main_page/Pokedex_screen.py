import asyncio
import time
from typing import Optional
import flet as ft

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from Custom_log import DEBUG_log


class Pokedex_screen(ft.Container):
    def __init__(
            self,
            text_color = "green",
            background_color = "black",
            frame_color = "grey",
            padding = 7,
            on_submit : Optional[callable] = None,
            prefix: Optional[ft.Control] = None,
            height : int = 70,
            on_change : Optional[callable] = None,
            value : Optional[str] = None,
            hint_text : Optional[str] = None
        ):

        self.on_submit = on_submit

        self._loading = False

        self._loading_icon = ft.Icon(
            "autorenew",
            color= text_color,
            animate_rotation= ft.Animation(300, ft.AnimationCurve.SLOW_MIDDLE),
            rotate= 0.
            )

        self.prefix = prefix
        if hasattr(prefix, "color"):
            self.prefix.color = text_color

        self.text_screen = ft.TextField(
            bgcolor= background_color,
            text_style= ft.TextStyle(font_family= "fira_mono", color=text_color, size= height/4),
            border_color= background_color,
            suffix = ft.IconButton("send", icon_color= text_color, on_click= on_submit),
            prefix= self.prefix,
            on_submit= on_submit,
            height= height,
            on_change= on_change,
            value= value,
            hint_text= hint_text,
            multiline= True,
            shift_enter= True
        )

        super().__init__(
            bgcolor= frame_color,
            padding= padding,
            content= self.text_screen,
            border_radius= 10,
            height= height,
            expand= True
        )

    async def _loading_animation(self):
        while self._loading:
            self._loading_icon.rotate += 3.14
            self._loading_icon.update()
            await asyncio.sleep(0.5)
    
    def start_loading(self, loading_text : str = "LOADING..."):
        self.text_screen.disabled = True
        self.text_screen.prefix = self._loading_icon
        self._temp_value = self.text_screen.value
        self.text_screen.value = " " + loading_text
        self.text_screen.update()
        if not self._loading:
            self._loading = True
            self._loading_task = self.page.run_task(self._loading_animation)

    def stop_loading(self):
        if self._loading:
            self._loading_task = None
            self._loading_icon.rotate = 0
            self._loading_icon.update()
        self._loading = False
        self.text_screen.value = self._temp_value
        self.text_screen.prefix = self.prefix
        self.text_screen.disabled = False
        self.text_screen.update()

    def did_mount(self):
        self.page.fonts ={
            "fira_mono" : "https://github.com/ryanoasis/nerd-fonts/raw/refs/heads/master/patched-fonts/FiraMono/Regular/FiraMonoNerdFont-Regular.otf"
        }
    

if __name__ == "__main__":
    def main(page: ft.Page):
        def process(e):
            poke.start_loading()
            time.sleep(1)
            poke.stop_loading()
            
        poke = Pokedex_screen(prefix= ft.Icon("ABC"), value= "test", on_submit= process)

        page.add(poke)
        

    ft.app(target=main)