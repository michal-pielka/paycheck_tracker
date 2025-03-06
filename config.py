import configparser


class Config:
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        self.refresh_rate = int(self.config["DEFAULT"]["refresh_rate"])
        self.bg_color = tuple(
            map(int, self.config["DEFAULT"]["background_color"].split(","))
        )
        self.fg_color = tuple(
            map(int, self.config["DEFAULT"]["foreground_color"].split(","))
        )
        self.width = int(self.config["DEFAULT"]["window_width"])
        self.height = int(self.config["DEFAULT"]["window_height"])
        self.hourly_rate = float(self.config["DEFAULT"]["hourly_rate"])
        self.decimal_digits = int(self.config["DEFAULT"]["decimal_digits"])
        self.milestone_multiple = int(
            self.config["DEFAULT"].get("milestone_multiple", 50)
        )
        # Clean effects by stripping whitespace and filter empty strings
        self.show_effects = (
            True if self.config["DEFAULT"]["show_effects"] == "true" else False
        )
        self.effects = [
            e.strip()
            for e in self.config["DEFAULT"].get("effects", "").split(",")
            if e.strip()
        ]
        self.effect_duration = int(self.config["DEFAULT"]["effect_duration"])
        self.glow_color = tuple(
            map(int, self.config["DEFAULT"]["glow_color"].split(","))
        )
        self.confetti_amount = int(self.config["DEFAULT"]["confetti_amount"])
        self.font = self.config["DEFAULT"]["font"]
        self.font_size = int(self.config["DEFAULT"]["font_size"])
        self.hide_menu_bar = (
            True if self.config["DEFAULT"]["hide_menu_bar"] == "true" else False
        )
