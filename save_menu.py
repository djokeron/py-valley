import arcade
import json
import os
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout 
data = "Data/"

class SaveMenu(arcade.View):
    "Меню сохранения"
    def __init__(self, game_state, volume):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        
        self.manager = UIManager()
        self.manager.enable()
        
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(space_between=10)
        self.setup_widgets()
        
        self.game = game_state
        self.volume = volume
        
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout) 

    def setup_widgets(self):
        file1_normal = arcade.load_texture(f"{data}Images/Buttons/file1_none.png")
        file1_hovered = arcade.load_texture(f"{data}Images/Buttons/file1_none_hovered.png")
        file1_pressed = arcade.load_texture(f"{data}Images/Buttons/file1_none_pressed.png")
        file1_button = UITextureButton(texture=file1_normal, 
                                         texture_hovered=file1_hovered,
                                         texture_pressed=file1_pressed,
                                         scale=1.0,)
        file2_normal = arcade.load_texture(f"{data}Images/Buttons/file2_none.png")
        file2_hovered = arcade.load_texture(f"{data}Images/Buttons/file2_none_hovered.png")
        file2_pressed = arcade.load_texture(f"{data}Images/Buttons/file2_none_pressed.png")
        file2_button = UITextureButton(texture=file2_normal, 
                                         texture_hovered=file2_hovered,
                                         texture_pressed=file2_pressed,
                                         scale=1.0,)
        file3_normal = arcade.load_texture(f"{data}Images/Buttons/file3_none.png")
        file3_hovered = arcade.load_texture(f"{data}Images/Buttons/file3_none_hovered.png")
        file3_pressed = arcade.load_texture(f"{data}Images/Buttons/file3_none_pressed.png")
        file3_button = UITextureButton(texture=file3_normal, 
                                         texture_hovered=file3_hovered,
                                         texture_pressed=file3_pressed,
                                         scale=1.0,)
        if os.path.exists(f"{data}Saved/save1.json"):
            file1_normal = arcade.load_texture(f"{data}Images/Buttons/file1_data.png")
            file1_hovered = arcade.load_texture(f"{data}Images/Buttons/file1_data_hovered.png")
            file1_pressed = arcade.load_texture(f"{data}Images/Buttons/file1_data_pressed.png")
            file1_button = UITextureButton(texture=file1_normal, 
                                           texture_hovered=file1_hovered,
                                           texture_pressed=file1_pressed,
                                           scale=1.0,) 
        if os.path.exists(f"{data}Saved/save2.json"):
            file2_normal = arcade.load_texture(f"{data}Images/Buttons/file2_data.png")
            file2_hovered = arcade.load_texture(f"{data}Images/Buttons/file2_data_hovered.png")
            file2_pressed = arcade.load_texture(f"{data}Images/Buttons/file2_data_pressed.png")
            file2_button = UITextureButton(texture=file2_normal, 
                                           texture_hovered=file2_hovered,
                                           texture_pressed=file2_pressed,
                                           scale=1.0,) 
        if os.path.exists(f"{data}Saved/save3.json"):
            file3_normal = arcade.load_texture(f"{data}Images/Buttons/file3_data.png")
            file3_hovered = arcade.load_texture(f"{data}Images/Buttons/file3_data_hovered.png")
            file3_pressed = arcade.load_texture(f"{data}Images/Buttons/file3_data_pressed.png")
            file3_button = UITextureButton(texture=file3_normal, 
                                           texture_hovered=file3_hovered,
                                           texture_pressed=file3_pressed,
                                           scale=1.0,) 
        self.box_layout.add(file1_button)
        self.box_layout.add(file2_button)
        self.box_layout.add(file3_button)
        file1_button.on_click = lambda event: self.save_data(1)
        file2_button.on_click = lambda event: self.save_data(2)
        file3_button.on_click = lambda event: self.save_data(3)
    
    def save_data(self, number_of_save):
        """Сохранение данных в файл json"""
        with open(f"{data}Saved/save{number_of_save}.json", "w") as save:
            json.dump(self.game.save_data, save)
    
    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from pause_menu import PauseMenu
            self.manager.disable()
            self.window.show_view(PauseMenu(self.game, self.volume))