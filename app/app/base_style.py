import pynecone as pc

# General styles.
BOLD_WEIGHT = "800"
PADDING_X = ["1em", "2em", "5em"]
PADDING_X2 = ["1em", "2em", "10em"]
HERO_FONT_SIZE = ["2em", "3em", "3em", "4em"]
H1_FONT_SIZE = ["2.2em", "2.4em", "2.5em"]
H2_FONT_SIZE = ["1.8em", "1.9em", "2em"]
H3_FONT_SIZE = "1.35em"
H4_FONT_SIZE = "1.1em"
TEXT_FONT_SIZE = "1em"
TEXT_FONT_FAMILY = "Inter"
CODE_FONT_FAMILY = "Fira Code, Fira Mono, Menlo, Consolas, DejaVu Sans Mono, monospace"
ACCENT_COLOR = "rgb(107,99,246)"
ACCENT_COLOR_LIGHT = "rgba(107,99,246, 0.4)"
ACCENT_COLOR_DARK = "rgb(86, 77, 209)"
SUBHEADING_COLOR = "rgb(37,50,56)"
LIGHT_TEXT_COLOR = "#94a3b8"

HEADER_LINK_STYLE = {"color": "white", "padding_right": "2em"}
ACTION_BUTTON_STYLE = {"padding": "1em", "bg": ACCENT_COLOR_DARK, "color": "white"}

# The base application style.
AppStyle = {
    "::selection": {
        "background_color": ACCENT_COLOR_LIGHT,
    },
    pc.Text: {
        "font_family": "Inter",
        "font_size": 16,
    },
    pc.Divider: {"margin_bottom": "1em", "margin_top": "0.5em"},
    pc.Code: {
        "color": ACCENT_COLOR,
    },
    "font_family": "Inter",
}

# Fonts to include.
STYLESHEETS = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap",
    "https://fonts.googleapis.com/css2?family=Silkscreen&display=swap",
]
