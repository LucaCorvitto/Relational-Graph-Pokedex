from typing import Optional
from flet import (Container, Text, Colors, BoxShadow)

class Text_decorator(Container):
    def __init__(
            self,
            text = None,
            text_color = Colors.BLACK,
            bg_color = Colors.WHITE,
            size: int = 13,
            on_click : Optional[callable] = None,
            expand : Optional [int | bool] = None,
            expand_loose : Optional [bool] = None,
        ) -> None:

        super().__init__(expand= expand, expand_loose = expand_loose)

        self.text = text
        self.text_color = text_color
        self.bgcolor = bg_color
        self.content = Text(self.text, color= self.text_color, size= size, weight= "bold", text_align="center")
        self.padding = (size)/1.3
        self.margin = 5
        self.opacity = 0.8
        self.border_radius = 20
        self.shadow= BoxShadow(spread_radius= 0.5, blur_radius= 3,)
        self.on_click = on_click