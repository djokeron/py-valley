import os
import sys
import arcade
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import main_menu

window = arcade.Window(800, 600, "py-valley")
volume_of_sounds = 1
menu_view = main_menu.MainMenu()
if __name__ == "__main__":
    window.show_view(menu_view)
    arcade.run()