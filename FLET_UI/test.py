from typing import Optional
import flet as ft
import asyncio
import aiohttp
import flet.canvas as cv

class Pokedex(ft.Container):

    def __init__(self, dimensions : float = 1.0):
        
        """
        The minimum dimensions value without breaking it is 0.25
        """

        super().__init__(
            expand=True,
            bgcolor=ft.Colors.RED,
            alignment=ft.alignment.top_center,
            border_radius= 50*dimensions,
            width=800 * dimensions,
            height = 1200 * dimensions,
            border= ft.Border(
                top= ft.BorderSide(
                    width= dimensions*10,
                    color= "black"
                ),
                left=ft.BorderSide(
                    width= dimensions*10,
                    color= "black"
                ),
            )
        )

        self.dimensions = dimensions

        self.selected_pokemon = 149

        button_dim = 80 * self.dimensions
        button_to_light_dim = 9/10
        light_dim = button_dim * button_to_light_dim

        border_radius = 50 * dimensions

        self.blue_light = ft.Container(
            width= light_dim,
            height= light_dim,
            bgcolor=ft.Colors.BLUE,
            border_radius=border_radius
        )
        
        self.blue_button = ft.Stack([
            ft.Container(
                width=button_dim,
                height=button_dim,
                bgcolor=ft.Colors.WHITE,
                border_radius=border_radius
            ),
            self.blue_light,
            ],
            alignment= ft.alignment.center
        )

        items_superior = [
            ft.Container(self.blue_button, width=button_dim, height=button_dim),
            ft.Container(width=button_dim/2, height=button_dim/2, bgcolor=ft.Colors.RED_200, border_radius=border_radius),
            ft.Container(width=button_dim/2, height=button_dim/2, bgcolor=ft.Colors.YELLOW, border_radius=border_radius),
            ft.Container(width=button_dim/2, height=button_dim/2, bgcolor=ft.Colors.GREEN, border_radius=border_radius),
        ]


        self.immagine = ft.Image(
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/132.png",
            scale=4* self.dimensions, # Redimensionamos a tamano muy grande
        )
        central_stack = ft.Stack(
            [
                ft.Container(
                    width=600 * self.dimensions,
                    height=400 * self.dimensions,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=20 * self.dimensions
                ),
                ft.Container(
                    width=550 * self.dimensions,
                    height=350 * self.dimensions,
                    bgcolor=ft.Colors.BLACK,
                ),
                self.immagine,
            ],
            alignment= ft.alignment.center
        )

        self.arrow = cv.Canvas([
            cv.Path(
                    [
                        cv.Path.MoveTo(40 * self.dimensions, 0),
                        cv.Path.LineTo(0,50 * self.dimensions),
                        cv.Path.LineTo(80 * self.dimensions, 50 * self.dimensions),
                    ],
                    paint=ft.Paint(
                        style=ft.PaintingStyle.FILL,
                    ),
                ),
            ],
            width=80 * self.dimensions,
            height=50 * self.dimensions,
        )

        self.focus_getter = ft.TextField(opacity= 0, height= 1, width=1)

        self.arrow_up = ft.Container(self.arrow, on_click=self.get_pokemon)
        self.arrow_down = ft.Container(self.arrow, rotate=ft.Rotate(angle=3.14159), on_click=self.get_pokemon)
        self.arrows = ft.Column([self.arrow_up, self.focus_getter, self.arrow_down], horizontal_alignment= ft.CrossAxisAlignment.CENTER)

        self.text = ft.Text(
            value="...",
            color=ft.Colors.BLACK,
            size=28 * self.dimensions,
        )

        items_inferior = [
            ft.Divider(thickness= 50 * self.dimensions),
            ft.Container(
                self.text,
                expand = 7,
                height = 400 * self.dimensions,
                padding=10 * self.dimensions,
                bgcolor=ft.Colors.GREEN,
                border_radius=20 * self.dimensions
            ),
            ft.Divider(thickness= 30 * self.dimensions),
            ft.Container(self.arrows, expand= 1, alignment= ft.alignment.center),
        ]
        
        superior = ft.Container(content=ft.Row(items_superior), padding= 50 * self.dimensions)
        center = ft.Container(central_stack, alignment=ft.alignment.center)
        inferior = ft.Container(content=ft.Row(items_inferior), padding= 50 * self.dimensions, alignment=ft.alignment.center)

        col = ft.Column(
            controls=[
                superior,
                center,
                inferior,
        ])

        self.content = col



    async def request(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
    
    async def get_pokemon(self, e: Optional[ft.ContainerTapEvent] = None, up: bool = True):
        if e is not None:
            if e.control == self.arrow_up:
                self.selected_pokemon += 1
            else:
                self.selected_pokemon -=1
        else:
            if up:
                self.selected_pokemon += 1
            else:
                self.selected_pokemon -= 1

        self.focus_getter.focus()
                
        numero = (self.selected_pokemon%150)+1
        resultado = await self.request(f"https://pokeapi.co/api/v2/pokemon/{numero}")

        datos = f"Number:{numero}\nName: {resultado['name']}\n\nAbilities:"
        for elemento in resultado['abilities']:
            
            habilidad = elemento['ability']['name']
            datos += f"\n{habilidad}"
        datos += f"\n\nHeight: {resultado['height']}"
        self.text.value = datos
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"
        self.immagine.src = sprite_url
        self.update()

    async def blink(self):
        while True:
            await asyncio.sleep(1)
            self.blue_light.bgcolor = ft.Colors.BLUE_100
            self.update()
            await asyncio.sleep(0.1)
            self.blue_light.bgcolor = ft.Colors.BLUE
            self.update()    
    
    async def on_key(self, e: ft.KeyboardEvent):
        if e.key == "Arrow Up":
            await self.get_pokemon(up= True)
        elif e.key == "Arrow Down":
            await self.get_pokemon(up= False)

    #to start and stop the blinking process
    def did_mount(self):
        self.page.on_keyboard_event = self.on_key
        self.blink_task = self.page.run_task(self.blink)
    
    def will_unmount(self):
        # This is called when the control is removed from the page
        if self.blink_task:
            self.blink_task.cancel()


if __name__ == "__main__":
    def main(page: ft.Page):
        # Initial scale value
        scale = 0.25

        # Container to hold the pokedex so we can update it
        pokedex_container = ft.Container()

        def on_slider_change(e):
            # Remove old pokedex and add a new one with updated scale
            pokedex_container.content = Pokedex(dimensions=e.control.value)
            print(e.control.value)
            page.update()

        slider = ft.Slider(
            min=0.25,
            max=1.0,
            value=scale,
            label="{value:.1f}",
            on_change=on_slider_change
        )

        # Set up the initial pokedex
        pokedex_container.content = Pokedex(dimensions=scale)

        page.scroll = "always"
        page.add(
            slider,
            pokedex_container
        )

    ft.app(target=main)