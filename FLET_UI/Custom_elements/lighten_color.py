from typing import Tuple
import colorsys

#full color dictionary
MATERIAL_COLOR_HEX = {
    # RED
    "red": "#f44336", "red50": "#ffebee", "red100": "#ffcdd2", "red200": "#ef9a9a",
    "red300": "#e57373", "red400": "#ef5350", "red500": "#f44336", "red600": "#e53935",
    "red700": "#d32f2f", "red800": "#c62828", "red900": "#b71c1c",
    "redaccent": "#ff1744", "redaccent100": "#ff8a80", "redaccent200": "#ff5252",
    "redaccent400": "#ff1744", "redaccent700": "#d50000",

    # PINK
    "pink": "#e91e63", "pink50": "#fce4ec", "pink100": "#f8bbd0", "pink200": "#f48fb1",
    "pink300": "#f06292", "pink400": "#ec407a", "pink500": "#e91e63", "pink600": "#d81b60",
    "pink700": "#c2185b", "pink800": "#ad1457", "pink900": "#880e4f",
    "pinkaccent": "#f50057", "pinkaccent100": "#ff80ab", "pinkaccent200": "#ff4081",
    "pinkaccent400": "#f50057", "pinkaccent700": "#c51162",

    # PURPLE
    "purple": "#9c27b0", "purple50": "#f3e5f5", "purple100": "#e1bee7", "purple200": "#ce93d8",
    "purple300": "#ba68c8", "purple400": "#ab47bc", "purple500": "#9c27b0", "purple600": "#8e24aa",
    "purple700": "#7b1fa2", "purple800": "#6a1b9a", "purple900": "#4a148c",
    "purpleaccent": "#d500f9", "purpleaccent100": "#ea80fc", "purpleaccent200": "#e040fb",
    "purpleaccent400": "#d500f9", "purpleaccent700": "#aa00ff",

    # DEEP PURPLE
    "deeppurple": "#673ab7", "deeppurple50": "#ede7f6", "deeppurple100": "#d1c4e9",
    "deeppurple200": "#b39ddb", "deeppurple300": "#9575cd", "deeppurple400": "#7e57c2",
    "deeppurple500": "#673ab7", "deeppurple600": "#5e35b1", "deeppurple700": "#512da8",
    "deeppurple800": "#4527a0", "deeppurple900": "#311b92",
    "deeppurpleaccent": "#651fff", "deeppurpleaccent100": "#b388ff",
    "deeppurpleaccent200": "#7c4dff", "deeppurpleaccent400": "#651fff",
    "deeppurpleaccent700": "#6200ea",

    # INDIGO
    "indigo": "#3f51b5", "indigo50": "#e8eaf6", "indigo100": "#c5cae9", "indigo200": "#9fa8da",
    "indigo300": "#7986cb", "indigo400": "#5c6bc0", "indigo500": "#3f51b5", "indigo600": "#3949ab",
    "indigo700": "#303f9f", "indigo800": "#283593", "indigo900": "#1a237e",
    "indigoaccent": "#304ffe", "indigoaccent100": "#8c9eff", "indigoaccent200": "#536dfe",
    "indigoaccent400": "#3d5afe", "indigoaccent700": "#304ffe",

    # BLUE
    "blue": "#2196f3", "blue50": "#e3f2fd", "blue100": "#bbdefb", "blue200": "#90caf9",
    "blue300": "#64b5f6", "blue400": "#42a5f5", "blue500": "#2196f3", "blue600": "#1e88e5",
    "blue700": "#1976d2", "blue800": "#1565c0", "blue900": "#0d47a1",
    "blueaccent": "#2962ff", "blueaccent100": "#82b1ff", "blueaccent200": "#448aff",
    "blueaccent400": "#2979ff", "blueaccent700": "#2962ff",

    # LIGHT BLUE
    "lightblue": "#03a9f4", "lightblue50": "#e1f5fe", "lightblue100": "#b3e5fc",
    "lightblue200": "#81d4fa", "lightblue300": "#4fc3f7", "lightblue400": "#29b6f6",
    "lightblue500": "#03a9f4", "lightblue600": "#039be5", "lightblue700": "#0288d1",
    "lightblue800": "#0277bd", "lightblue900": "#01579b",
    "lightblueaccent": "#00b0ff", "lightblueaccent100": "#80d8ff",
    "lightblueaccent200": "#40c4ff", "lightblueaccent400": "#00b0ff",
    "lightblueaccent700": "#0091ea",

    # CYAN
    "cyan": "#00bcd4", "cyan50": "#e0f7fa", "cyan100": "#b2ebf2", "cyan200": "#80deea",
    "cyan300": "#4dd0e1", "cyan400": "#26c6da", "cyan500": "#00bcd4", "cyan600": "#00acc1",
    "cyan700": "#0097a7", "cyan800": "#00838f", "cyan900": "#006064",
    "cyanaccent": "#00e5ff", "cyanaccent100": "#84ffff", "cyanaccent200": "#18ffff",
    "cyanaccent400": "#00e5ff", "cyanaccent700": "#00b8d4",

    # TEAL
    "teal": "#009688", "teal50": "#e0f2f1", "teal100": "#b2dfdb", "teal200": "#80cbc4",
    "teal300": "#4db6ac", "teal400": "#26a69a", "teal500": "#009688", "teal600": "#00897b",
    "teal700": "#00796b", "teal800": "#00695c", "teal900": "#004d40",
    "tealaccent": "#1de9b6", "tealaccent100": "#a7ffeb", "tealaccent200": "#64ffda",
    "tealaccent400": "#1de9b6", "tealaccent700": "#00bfa5",

    # GREEN
    "green": "#4caf50", "green50": "#e8f5e9", "green100": "#c8e6c9", "green200": "#a5d6a7",
    "green300": "#81c784", "green400": "#66bb6a", "green500": "#4caf50", "green600": "#43a047",
    "green700": "#388e3c", "green800": "#2e7d32", "green900": "#1b5e20",
    "greenaccent": "#00c853", "greenaccent100": "#b9f6ca", "greenaccent200": "#69f0ae",
    "greenaccent400": "#00e676", "greenaccent700": "#00c853",

    # LIGHT GREEN
    "lightgreen": "#8bc34a", "lightgreen50": "#f1f8e9", "lightgreen100": "#dcedc8",
    "lightgreen200": "#c5e1a5", "lightgreen300": "#aed581", "lightgreen400": "#9ccc65",
    "lightgreen500": "#8bc34a", "lightgreen600": "#7cb342", "lightgreen700": "#689f38",
    "lightgreen800": "#558b2f", "lightgreen900": "#33691e",
    "lightgreenaccent": "#64dd17", "lightgreenaccent100": "#ccff90",
    "lightgreenaccent200": "#b2ff59", "lightgreenaccent400": "#76ff03",
    "lightgreenaccent700": "#64dd17",

    # LIME
    "lime": "#cddc39", "lime50": "#f9fbe7", "lime100": "#f0f4c3", "lime200": "#e6ee9c",
    "lime300": "#dce775", "lime400": "#d4e157", "lime500": "#cddc39", "lime600": "#c0ca33",
    "lime700": "#afb42b", "lime800": "#9e9d24", "lime900": "#827717",
    "limeaccent": "#aeea00", "limeaccent100": "#f4ff81", "limeaccent200": "#eeff41",
    "limeaccent400": "#c6ff00", "limeaccent700": "#aeea00",

    # YELLOW
    "yellow": "#ffeb3b", "yellow50": "#fffde7", "yellow100": "#fff9c4",
    "yellow200": "#fff59d", "yellow300": "#fff176", "yellow400": "#ffee58",
    "yellow500": "#ffeb3b", "yellow600": "#fdd835", "yellow700": "#fbc02d",
    "yellow800": "#f9a825", "yellow900": "#f57f17",
    "yellowaccent": "#ffd600", "yellowaccent100": "#ffff8d", "yellowaccent200": "#ffff00",
    "yellowaccent400": "#ffea00", "yellowaccent700": "#ffd600",

    # AMBER
    "amber": "#ffc107", "amber50": "#fff8e1", "amber100": "#ffecb3", "amber200": "#ffe082",
    "amber300": "#ffd54f", "amber400": "#ffca28", "amber500": "#ffc107", "amber600": "#ffb300",
    "amber700": "#ffa000", "amber800": "#ff8f00", "amber900": "#ff6f00",
    "amberaccent": "#ffab00", "amberaccent100": "#ffe57f", "amberaccent200": "#ffd740",
    "amberaccent400": "#ffc400", "amberaccent700": "#ffab00",

    # ORANGE
    "orange": "#ff9800", "orange50": "#fff3e0", "orange100": "#ffe0b2", "orange200": "#ffcc80",
    "orange300": "#ffb74d", "orange400": "#ffa726", "orange500": "#ff9800", "orange600": "#fb8c00",
    "orange700": "#f57c00", "orange800": "#ef6c00", "orange900": "#e65100",
    "orangeaccent": "#ff9100", "orangeaccent100": "#ffd180", "orangeaccent200": "#ffab40",
    "orangeaccent400": "#ff9100", "orangeaccent700": "#ff6d00",

    # DEEP ORANGE
    "deeporange": "#ff5722", "deeporange50": "#fbe9e7", "deeporange100": "#ffccbc",
    "deeporange200": "#ffab91", "deeporange300": "#ff8a65", "deeporange400": "#ff7043",
    "deeporange500": "#ff5722", "deeporange600": "#f4511e", "deeporange700": "#e64a19",
    "deeporange800": "#d84315", "deeporange900": "#bf360c",
    "deeporangeaccent": "#ff3d00", "deeporangeaccent100": "#ff9e80",
    "deeporangeaccent200": "#ff6e40", "deeporangeaccent400": "#ff3d00",
    "deeporangeaccent700": "#dd2c00",

    # BROWN
    "brown": "#795548", "brown50": "#efebe9", "brown100": "#d7ccc8", "brown200": "#bcaaa4",
    "brown300": "#a1887f", "brown400": "#8d6e63", "brown500": "#795548",
    "brown600": "#6d4c41", "brown700": "#5d4037", "brown800": "#4e342e",
    "brown900": "#3e2723",

    # GREY
    "grey": "#9e9e9e", "grey50": "#fafafa", "grey100": "#f5f5f5", "grey200": "#eeeeee",
    "grey300": "#e0e0e0", "grey400": "#bdbdbd", "grey500": "#9e9e9e",
    "grey600": "#757575", "grey700": "#616161", "grey800": "#424242",
    "grey900": "#212121",

    # BLUE GREY
    "bluegrey": "#607d8b", "bluegrey50": "#eceff1", "bluegrey100": "#cfd8dc",
    "bluegrey200": "#b0bec5", "bluegrey300": "#90a4ae", "bluegrey400": "#78909c",
    "bluegrey500": "#607d8b", "bluegrey600": "#546e7a", "bluegrey700": "#455a64",
    "bluegrey800": "#37474f", "bluegrey900": "#263238",
}


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert #rrggbb to (r,g,b)."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert (r,g,b) to #rrggbb."""
    return f"#{r:02x}{g:02x}{b:02x}"

def lighten_color(color: str, factor: float = 0.3) -> str:
    """
    Lighten a Flet color name or hex string.
    factor: 0 to 1, how much to move towards white.
    Returns hex string.
    """
    color_key = color.lower()
    if color_key in MATERIAL_COLOR_HEX:
        hex_color = MATERIAL_COLOR_HEX[color_key]
    elif color_key.startswith("#"):
        hex_color = color_key
    else:
        raise ValueError(f"Unknown color: {color}")

    r, g, b = hex_to_rgb(hex_color)
    # Convert to HLS for easy lightening
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    l = min(1, l + (1-l) * factor)
    r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)
    return rgb_to_hex(int(r2*255), int(g2*255), int(b2*255))

# Example usage:
if __name__ == "__main__":
    base = "red500"  # or ft.Colors.RED_500 if you convert to string
    lighter = lighten_color(base, 0.5)
    print(f"Base: {base} -> Lighter: {lighter}")

    # With direct hex
    print(lighten_color("#2196f3", 0.2))
