import asyncio
import flet as ft

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Main_page.starting_page import Starting_page
from FLET_UI.Main_page.Top_navigation import TopNavigationPokedex
from FLET_UI.Main_page.Bottom_pokedex import BottomPokedex
from FLET_UI.Main_page.visual_page import Main_structure

CURRENT_PAGE : ft.Container = None

if __name__ == "__main__":
    def main(page: ft.Page):
        global CURRENT_PAGE
        page.title = "POKEDEX"
        page.route = "/main_page"

        def submit_query(e: ft.ControlEvent):
            """
            insert query in e.control.data
            """
            query :str = e.control.data
            page.go(f"/query={query}")

        def change_route(e: ft.ControlEvent):
            page.go("/main_page")

        navigation = TopNavigationPokedex(width_page_ratio= 0.5,on_expand_query= change_route)
        starting_page = Starting_page(on_submit_query= submit_query)
        query_page = Main_structure()
        bottom_nav = BottomPokedex()

        CURRENT_PAGE = starting_page
        page.spacing = 0

        page.add(navigation)
        page.overlay.append(bottom_nav)
        page.update()

        def query_page_go(query):
            if CURRENT_PAGE == query_page:
                return
            page.controls.remove(CURRENT_PAGE)
            navigation.show_query_field(query)
            CURRENT_PAGE = query_page
            page.add(query_page)

        def main_page_go(query):
            if CURRENT_PAGE == starting_page:
                return
            page.controls.remove(CURRENT_PAGE)
            navigation.hide_query_field()
            page.add(starting_page)
            starting_page.input_box.value = query
            CURRENT_PAGE = starting_page

        def animate_page_change(on_half: callable, on_end: callable):
            navigation.on_animation_end = on_end
            navigation.animate_open_close(on_half_animation= on_half)
            bottom_nav.animate_open_close()

        async def route_change(e: ft.ControlEvent):
            await asyncio.sleep(0.5)
            animate_page_change(on_half= lambda _: page.add(CURRENT_PAGE), on_end= lambda _: print("fired"))

            if page.route == "/main_page":
                query = navigation.query_field.value if navigation.query_field.visible else None
                #main_page_go(query)

            if page.route.startswith("/query="):
                query = starting_page.input_box.value
                #query_page_go(query)


        page.on_route_change = route_change
        

    ft.app(target=main)