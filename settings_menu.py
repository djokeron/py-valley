import arcade
import json
import sys
import main_menu
from arcade.gui import UIManager, UISlider, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout 
data = "Data/"


class SettingsMenu(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        
        self.manager = UIManager()
        self.manager.enable()
        
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(space_between=10)
        self.setup_widgets()
        
        self.game_state = None
        
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout) 

    def setup_widgets(self):
        Volume_label = UILabel(text="Звук", 
                    font_size=20, 
                    text_color=arcade.color.WHITE, 
                    width=300, 
                    align="center") 
        Sound_slider = UISlider(width=200, height=20, min_value=0, max_value=100, value=100)
        self.box_layout.add(Volume_label) 
        self.box_layout.add(Sound_slider) 
    
    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.manager.disable()
            self.window.show_view(main_menu.MainMenu())