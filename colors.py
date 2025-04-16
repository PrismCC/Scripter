from catppuccin import PALETTE
from catppuccin.models import RGB


class Colors:
    rosewater = None
    flamingo = None
    pink = None
    mauve = None
    red = None
    maroon = None
    peach = None
    yellow = None
    green = None
    teal = None
    sky = None
    sapphire = None
    blue = None
    lavender = None
    text = None
    subtext1 = None
    subtext0 = None
    overlay2 = None
    overlay1 = None
    overlay0 = None
    surface2 = None
    surface1 = None
    surface0 = None
    base = None
    mantle = None
    crust = None

    def __init__(self, name, light_rgb: RGB, dark_rgb: RGB):
        self.name = name
        self.light_r = light_rgb.r
        self.light_g = light_rgb.g
        self.light_b = light_rgb.b
        self.dark_r = dark_rgb.r
        self.dark_g = dark_rgb.g
        self.dark_b = dark_rgb.b

    @property
    def light_rgb(self):
        return self.light_r, self.light_g, self.light_b

    @property
    def dark_rgb(self):
        return self.dark_r, self.dark_g, self.dark_b

    @property
    def light_hex(self):
        return f"#{self.light_r:02x}{self.light_g:02x}{self.light_b:02x}"

    @property
    def dark_hex(self):
        return f"#{self.dark_r:02x}{self.dark_g:02x}{self.dark_b:02x}"

    @property
    def hex_tuple(self):
        return self.light_hex, self.dark_hex


# 参考Catppuccin作为预设颜色
Colors.rosewater = Colors("rosewater", PALETTE.latte.colors.rosewater.rgb, PALETTE.macchiato.colors.rosewater.rgb)
Colors.flamingo = Colors("flamingo", PALETTE.latte.colors.flamingo.rgb, PALETTE.macchiato.colors.flamingo.rgb)
Colors.pink = Colors("pink", PALETTE.latte.colors.pink.rgb, PALETTE.macchiato.colors.pink.rgb)
Colors.mauve = Colors("mauve", PALETTE.latte.colors.mauve.rgb, PALETTE.macchiato.colors.mauve.rgb)
Colors.red = Colors("red", PALETTE.latte.colors.red.rgb, PALETTE.macchiato.colors.red.rgb)
Colors.maroon = Colors("maroon", PALETTE.latte.colors.maroon.rgb, PALETTE.macchiato.colors.maroon.rgb)
Colors.peach = Colors("peach", PALETTE.latte.colors.peach.rgb, PALETTE.macchiato.colors.peach.rgb)
Colors.yellow = Colors("yellow", PALETTE.latte.colors.yellow.rgb, PALETTE.macchiato.colors.yellow.rgb)
Colors.green = Colors("green", PALETTE.latte.colors.green.rgb, PALETTE.macchiato.colors.green.rgb)
Colors.teal = Colors("teal", PALETTE.latte.colors.teal.rgb, PALETTE.macchiato.colors.teal.rgb)
Colors.sky = Colors("sky", PALETTE.latte.colors.sky.rgb, PALETTE.macchiato.colors.sky.rgb)
Colors.sapphire = Colors("sapphire", PALETTE.latte.colors.sapphire.rgb, PALETTE.macchiato.colors.sapphire.rgb)
Colors.blue = Colors("blue", PALETTE.latte.colors.blue.rgb, PALETTE.macchiato.colors.blue.rgb)
Colors.lavender = Colors("lavender", PALETTE.latte.colors.lavender.rgb, PALETTE.macchiato.colors.lavender.rgb)
Colors.text = Colors("text", PALETTE.latte.colors.text.rgb, PALETTE.macchiato.colors.text.rgb)
Colors.subtext1 = Colors("subtext1", PALETTE.latte.colors.subtext1.rgb, PALETTE.macchiato.colors.subtext1.rgb)
Colors.subtext0 = Colors("subtext0", PALETTE.latte.colors.subtext0.rgb, PALETTE.macchiato.colors.subtext0.rgb)
Colors.overlay2 = Colors("overlay2", PALETTE.latte.colors.overlay2.rgb, PALETTE.macchiato.colors.overlay2.rgb)
Colors.overlay1 = Colors("overlay1", PALETTE.latte.colors.overlay1.rgb, PALETTE.macchiato.colors.overlay1.rgb)
Colors.overlay0 = Colors("overlay0", PALETTE.latte.colors.overlay0.rgb, PALETTE.macchiato.colors.overlay0.rgb)
Colors.surface2 = Colors("surface2", PALETTE.latte.colors.surface2.rgb, PALETTE.macchiato.colors.surface2.rgb)
Colors.surface1 = Colors("surface1", PALETTE.latte.colors.surface1.rgb, PALETTE.macchiato.colors.surface1.rgb)
Colors.surface0 = Colors("surface0", PALETTE.latte.colors.surface0.rgb, PALETTE.macchiato.colors.surface0.rgb)
Colors.base = Colors("base", PALETTE.latte.colors.base.rgb, PALETTE.macchiato.colors.base.rgb)
Colors.mantle = Colors("mantle", PALETTE.latte.colors.mantle.rgb, PALETTE.macchiato.colors.mantle.rgb)
Colors.crust = Colors("crust", PALETTE.latte.colors.crust.rgb, PALETTE.macchiato.colors.crust.rgb)
