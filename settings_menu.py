import arcade
import json
import main_menu
from arcade.gui import UIManager, UISlider, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout 
data = "Data/"


class SettingsMenu(arcade.View):
    def __init__(self, volume=[1, 1, 1]):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        self.volume = volume
        
        self.manager = UIManager()
        self.manager.enable()
        
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(space_between=10)
        self.setup_widgets()
        
        self.game_state = None

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout) 
        
    def setup_widgets(self):
        Master_label = UILabel(text="Громкость Общая", 
                    font_size=20, 
                    text_color=arcade.color.WHITE, 
                    width=300, 
                    align="center") 
        Sound_Master_slider = UISlider(width=200, height=20, min_value=0, max_value=100, value=self.volume[0]*100)
        
        Sounds_label = UILabel(text="Звуки", 
                    font_size=20, 
                    text_color=arcade.color.WHITE, 
                    width=300, 
                    align="center") 
        Sounds_slider = UISlider(width=200, height=20, min_value=0, max_value=100, value=self.volume[1]*100)
        
        Music_label = UILabel(text="Музыка", 
                    font_size=20, 
                    text_color=arcade.color.WHITE, 
                    width=300, 
                    align="center") 
        Music_slider = UISlider(width=200, height=20, min_value=0, max_value=100, value=self.volume[2]*100)
        
        self.box_layout.add(Master_label) 
        self.box_layout.add(Sound_Master_slider)
        self.box_layout.add(Sounds_label) 
        self.box_layout.add(Sounds_slider)
        self.box_layout.add(Music_label) 
        self.box_layout.add(Music_slider)
        Sound_Master_slider.on_change = lambda event: self.change_volume(Sound_Master_slider.value)
        Sounds_slider.on_change = lambda event: self.change_volume(Sounds_slider.value, "sounds")
        Music_slider.on_change = lambda event: self.change_volume(Music_slider.value, "music")
    
    def change_volume(self, value, sound="master"):
        if sound == "master":
            self.volume[0] = value / 100
        elif sound == "sounds":
            self.volume[1] = value / 100
        elif sound == "music":
            self.volume[2] = value / 100
        with open(f"{data}settings.json", "w") as settings:
            json.dump(self.volume, settings)
             
    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.manager.disable()
            self.window.show_view(main_menu.MainMenu(self.volume))