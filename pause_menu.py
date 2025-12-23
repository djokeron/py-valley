import arcade
import main_menu
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout 


class PauseMenu(arcade.View):
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
        MainMenu_normal = arcade.load_texture("Images/Buttons/MainMenu_Normal.png")
        MainMenu_hovered = arcade.load_texture("Images/Buttons/MainMenu_Hovered.png")
        MainMenu_pressed = arcade.load_texture("Images/Buttons/MainMenu.png")
        MainMenu_button = UITextureButton(texture=MainMenu_normal, 
                                         texture_hovered=MainMenu_hovered,
                                         texture_pressed=MainMenu_pressed,
                                         scale=1.0,)
        Save_normal = arcade.load_texture("Images/Buttons/Save_Normal.png")
        Save_hovered = arcade.load_texture("Images/Buttons/Save_Hovered.png")
        Save_pressed = arcade.load_texture("Images/Buttons/Save.png")
        Save_button = UITextureButton(texture=Save_normal, 
                                      texture_hovered=Save_hovered,
                                      texture_pressed=Save_pressed,
                                      scale=1.0,)
        Load_normal = arcade.load_texture("Images/Buttons/Load_Normal.png")
        Load_hovered = arcade.load_texture("Images/Buttons/Load_Hovered.png")
        Load_pressed = arcade.load_texture("Images/Buttons/Load.png")
        Load_button = UITextureButton(texture=Load_normal, 
                                      texture_hovered=Load_hovered,
                                      texture_pressed=Load_pressed,
                                      scale=1.0,)
        self.box_layout.add(MainMenu_button)
        self.box_layout.add(Save_button)
        self.box_layout.add(Load_button)
        MainMenu_button.on_click = lambda x: self.window.show_view(main_menu.MainMenu())
        
    def on_draw(self):
        self.clear()
        self.manager.draw()  # Рисуй GUI поверх всего

    def on_mouse_press(self, x, y, button, modifiers):
        pass  # Для кликов, но manager сам обрабатывает