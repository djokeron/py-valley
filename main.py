import os
import sys
import arcade
import json
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import main_menu

window = arcade.Window(800, 600, "py-valley")
volume_of_sounds = 1
if os.path.exists("Data/settings.json"):
    with open("Data/settings.json", "r") as s: 
        volume_of_sounds = json.load(s)
menu_view = main_menu.MainMenu(volume_of_sounds)
if __name__ == "__main__":
    window.show_view(menu_view)
    arcade.run()