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

        def submit_query(e: ft.ControlEvent):
            """
            insert query in e.control.data
            """
            query :str = e.control.data
            page.go(f"/query={query}")

        def change_route(e: ft.ControlEvent):
            page.go("/main_page")

        navigation = TopNavigationPokedex(on_expand_query= change_route)
        starting_page = Starting_page(on_submit_query= submit_query)
        query_page = Main_structure()

        page.add(navigation)
        page.add(starting_page)

        def query_page_go(query):
            if query_page in page.controls:
                return
            page.controls.pop()
            navigation.show_query_field(query)
            page.add(query_page)

        def main_page_go(query):
            if starting_page in page.controls:
                return
            page.controls.pop()
            navigation.hide_query_field()
            page.add(starting_page)
            starting_page.offset = ft.Offset(0, -1.5)
            page.update()
            starting_page.input_box.value = query
            starting_page.animate_in()

        def route_change(e: ft.ControlEvent):

            if page.route == "/main_page":
                query = navigation.query_field.value if navigation.query_field.visible else None
                main_page_go(query)

            if page.route.startswith("/query="):
                query = starting_page.input_box.value
                starting_page.on_animation_end = lambda _: query_page_go(query)
                starting_page.animate_out()

        page.on_route_change = route_change

    ft.app(target=main)