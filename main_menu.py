import arcade
import game
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout 


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        
        self.manager = UIManager()
        self.manager.enable()
        
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.setup_widgets()
        
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout) 

    def setup_widgets(self):
        NewGame_normal = arcade.load_texture("Images/Buttons/NewGameNormal.png")
        NewGame_hovered = arcade.load_texture("Images/Buttons/NewGame_Hovered.png")
        NewGame_pressed = arcade.load_texture("Images/Buttons/NewGame.png")
        NewGame_button = UITextureButton(texture=NewGame_normal, 
                                         texture_hovered=NewGame_hovered,
                                         texture_pressed=NewGame_pressed,
                                         scale=1.0,)
        Load_normal = arcade.load_texture("Images/Buttons/Load_Normal.png")
        Load_hovered = arcade.load_texture("Images/Buttons/Load_Hovered.png")
        Load_pressed = arcade.load_texture("Images/Buttons/Load.png")
        Load_button = UITextureButton(texture=Load_normal, 
                                      texture_hovered=Load_hovered,
                                      texture_pressed=Load_pressed,
                                      scale=1.0,)
        Settings_normal = arcade.load_texture("Images/Buttons/Settings_Normal.png")
        Settings_hovered = arcade.load_texture("Images/Buttons/Settings_Hovered.png")
        Settings_pressed = arcade.load_texture("Images/Buttons/Settings.png")
        Settings_button = UITextureButton(texture=Settings_normal, 
                                          texture_hovered=Settings_hovered,
                                          texture_pressed=Settings_pressed,
                                          scale=1.0,)
        self.box_layout.add(NewGame_button)
        self.box_layout.add(Load_button)
        self.box_layout.add(Settings_button)
        
        NewGame_button.on_click = lambda x: self.window.show_view(game.Game())
        
    def on_draw(self):
        self.clear()
        self.manager.draw()
