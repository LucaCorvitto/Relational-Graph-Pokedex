import flet as ft

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Main_page.starting_page import Starting_page
from FLET_UI.Main_page.Top_navigation import TopNavigationPokedex
from FLET_UI.Main_page.visual_page import Main_structure

if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "POKEDEX"
        page.route = "/main_page"

        def change_route(e: ft.ControlEvent):
            """
            insert query in e.control.data
            """
            page.go(f"/query={e.control.data}")

        navigation = TopNavigationPokedex()
        starting_page = Starting_page(on_submit_query= change_route)
        target_page = Main_structure()

        page.add(navigation)
        page.add(starting_page)

        def route_change(e: ft.ControlEvent):

            def change_page(target):
                page.controls.pop()
                page.add(target)

            if page.route.startswith("/query="):
            # make sure we set the handler to a function, not to the result of page.add
                starting_page.on_animation_end = lambda _: change_page(target_page)
                starting_page.animate_out()

        page.on_route_change = route_change

    ft.app(target=main)