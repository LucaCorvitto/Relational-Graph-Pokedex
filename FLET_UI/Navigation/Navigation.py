import time
import flet as ft

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Main_page.Top_navigation_Pokedex import TopNavigationPokedex
from FLET_UI.Main_page.Bottom_pokedex import BottomPokedex
from FLET_UI.Main_page.visual_page import Main_structure
# import my_langgraph_definition as LLM
from utils import build_graph, run_pokemon_query

WEB_VIEW = True
CURRENT_PAGE : ft.Container = None
QUERY_DELIMITER = '#'

if __name__ == "__main__":

    def crate_query_page(page: ft.Page, query: str):
        return Main_structure(query)

    def main(page: ft.Page):
        global CURRENT_PAGE
        page.title = "POKEDEX"
        page.route = "/main_page"
        pokemon_graph_agent, pokemon_names, driver = build_graph()

        def submit_query(e: ft.ControlEvent):
            """
            insert query in e.control.data
            """
            query :str = navigation.query_field.text_screen.value
            if query is not None:
                query = query.replace('\n', QUERY_DELIMITER)
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

        def open_pokedex(query):
            if navigation.expanded_view:
                navigation.start_processing_query_animation(loading_text = "Generating response...")
                time.sleep(1)
                #insert query to LLM
                run_pokemon_query(query, pokemon_graph_agent, pokemon_names, driver)
                navigation.stop_processing_query_animation()
                navigation.hide_body()
                navigation.show_hide_expand_query()
                bottom_nav.open()

        def close_pokedex():
                navigation.show_body()
                navigation.show_hide_expand_query()
                bottom_nav.close()

        def route_change(e: ft.ControlEvent):

            def extract_query(input_str: str, prefix="/query=", delimiter="#", replacement="\n") -> str:
                return input_str[len(prefix):].replace(delimiter, replacement)

            if page.route == "/main_page":
                if CURRENT_PAGE == starting_page:
                    return
                change_page(starting_page)
                close_pokedex()

            if page.route.startswith("/query="):
                query = extract_query(page.route, delimiter= QUERY_DELIMITER)
                navigation.set_query(query)
                open_pokedex(query)
                change_page(crate_query_page(page, query))

            else:
                page.go("/main_page")

        page.on_route_change = route_change
        
    ft.app(target=main, view= ft.AppView.WEB_BROWSER if WEB_VIEW else ft.AppView.FLET_APP)