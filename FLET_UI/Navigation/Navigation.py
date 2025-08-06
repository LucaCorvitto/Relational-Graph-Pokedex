import time
import flet as ft
import urllib.parse

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from FLET_UI.Main_page.Top_navigation_Pokedex import TopNavigationPokedex
from FLET_UI.Main_page.Bottom_pokedex import BottomPokedex
from FLET_UI.Main_page.visual_page import Main_structure
from utils import build_graph, run_pokemon_query

WEB_VIEW = True
CURRENT_PAGE : ft.Container = None

if __name__ == "__main__":

    def crate_query_page(page: ft.Page, query: str, answer: str):
        return Main_structure(query=query, response=answer)

    def create_error_page(error: str):
        return ft.Container(
            content= ft.Text(f"ERROR: {error}", size= 25, weight= "bold"),
            alignment= ft.alignment.center,
            expand= True
        )

    def main(page: ft.Page):
        global CURRENT_PAGE
        page.title = "POKEDEX"
        page.route = "/main_page"
        page.window.width = 500
        page.window.height = 700

        def handle_error(e):
            encoded_error = urllib.parse.quote(str (e))
            page.go(f"/Error={encoded_error}")  

        def submit_query(e: ft.ControlEvent):
            query: str = navigation.query_field.text_screen.value
            if query:
                encoded_query = urllib.parse.quote(query)
                page.go(f"/query={encoded_query}")  

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

        page.overlay.append(bottom_nav)
        page.add(navigation)
        page.add(CURRENT_PAGE)
        page.update()

        navigation.start_processing_query_animation(loading_text = "Initialising...")
        try:
            pokemon_graph_agent, pokemon_names, driver = build_graph()
        except Exception as e:
            handle_error(e)
            print(e)
        navigation.stop_processing_query_animation()

        def change_page(target_page):
            global CURRENT_PAGE
            if CURRENT_PAGE == target_page:
                return
            page.controls.remove(CURRENT_PAGE)
            CURRENT_PAGE = target_page
            page.add(target_page)
        
        def open_pokedex() -> str:
            if navigation.expanded_view:
                if navigation.processing:
                    navigation.stop_processing_query_animation()
                navigation.hide_body()
                navigation.toggle_expand_query()
                bottom_nav.open()

        def process_query(query) -> str:
            if navigation.expanded_view:
                navigation.start_processing_query_animation(loading_text = "Generating response...")
                #insert query to LLM
                answer = run_pokemon_query(query, pokemon_graph_agent, pokemon_names, driver)
                #return LLM response to generate next page
                return answer["response"]

        def close_pokedex():
                navigation.show_body()
                navigation.toggle_expand_query()
                bottom_nav.close()

        def route_change(e: ft.ControlEvent):

            def extract_query(input_str: str, prefix="/query=") -> str:
                return urllib.parse.unquote(input_str[len(prefix):])

            if page.route == "/main_page":
                if CURRENT_PAGE == starting_page:
                    return
                change_page(starting_page)
                close_pokedex()

            elif page.route.startswith("/query="):
                query = extract_query(page.route)
                navigation.set_query(query)
                answer = process_query(query)
                change_page(crate_query_page(page, query= query, answer= answer))
                open_pokedex()

            elif page.route.startswith("/Error="):
                error = extract_query(page.route, "/Error=")
                change_page(create_error_page(error= error))
                open_pokedex()

            else:
                page.go("/main_page")

        page.on_route_change = route_change
        
    ft.app(target=main, view= ft.AppView.WEB_BROWSER if WEB_VIEW else ft.AppView.FLET_APP)