import asyncio
import time
import flet as ft

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Main_page.starting_page import Starting_page
from FLET_UI.Main_page.Top_navigation_Pokedex import TopNavigationPokedex
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
            query :str = navigation.query_field.text_screen.value
            page.go(f"/query={query}")

        def change_route(e: ft.ControlEvent):
            page.go("/main_page")

        navigation = TopNavigationPokedex(
            width_page_ratio= 0.5,
            on_expand_query= change_route,
            on_submit_query= submit_query,
            height_page_ratio= 4/5
            )
        starting_page = ft.Container(bgcolor= "green")
        query_page = Main_structure()
        bottom_nav = BottomPokedex(color= ft.Colors.GREY_100, height_page_ratio= 1/5)

        CURRENT_PAGE = starting_page
        page.spacing = 0

        page.window.width = 351
        page.window.height = 500
        page.overlay.append(bottom_nav)
        page.add(navigation)
        page.add(CURRENT_PAGE)
        page.update()

        def change_page(target_page):
            global CURRENT_PAGE
            if CURRENT_PAGE == target_page:
                return
            page.controls.remove(CURRENT_PAGE)
            CURRENT_PAGE = target_page
            page.add(target_page)

        def open_pokedex():
            if navigation.expanded_view:
                navigation.start_processing_query_animation(loading_text = "Generating response...")
                time.sleep(3)
                navigation.stop_processing_query_animation()
                navigation.hide_body()
                navigation.show_hide_expand_query()
                bottom_nav.open()

        def close_pokedex():
                navigation.show_body()
                navigation.show_hide_expand_query()
                bottom_nav.close()


        def route_change(e: ft.ControlEvent):

            if page.route == "/main_page":
                if CURRENT_PAGE == starting_page:
                    return
                change_page(starting_page)
                close_pokedex()

            if page.route.startswith("/query="):
                change_page(query_page)
                open_pokedex()

        page.on_route_change = route_change
        

    ft.app(target=main)