import time
from typing import Optional
import flet as ft

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Main_page.Bottom_pokedex import BottomPokedex
from FLET_UI.Main_page.Top_navigation_Pokedex import TopNavigationPokedex

if __name__ == "__main__":
    def main(page: ft.Page):

        page.window.width = 351
        page.window.height = 500
        page.window.min_height = 400
        page.window.min_width = 300

        # This triggers after did_mount has placed structure in overlay
        def move(e):
            poke.show_query_field("lol")
            poke.on_animation_end = lambda _: print("finito!")
            poke.animate_open_close(-0.5, on_half_animation= lambda _: print("siamo a meta'!"))
        
        def process(e):
            if poke.expanded_view:
                poke.start_processing_query_animation(loading_text = "Generating response...")
                time.sleep(3)
                poke.stop_processing_query_animation()
                poke.hide_body()
                bottom._animate_scrolling(-20)

            else:
                poke.show_body()
                bottom._animate_scrolling(0)


        poke = TopNavigationPokedex(on_submit_query= process, height_page_ratio= 4/5)
        bottom = BottomPokedex(height_page_ratio=1/5, color="white")
        page.overlay.append(bottom)

        page.add(poke)
        

    ft.app(target=main)