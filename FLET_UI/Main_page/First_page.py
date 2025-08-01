import asyncio
import time
from typing import Optional
import flet as ft
import flet.canvas as cv

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
        
        def lighting(e):
            poke.processing_query_animation()

        poke = TopNavigationPokedex(on_submit_query= lighting, height_page_ratio= 4/5)

        page.overlay.append(BottomPokedex(height_page_ratio=1/5, color="blue"))

        page.add(poke)
        

    ft.app(target=main)