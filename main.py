import os
import sys
import arcade
import json
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import main_menu

window = arcade.Window(800, 600, "py-valley")

volume_all = [1, 1, 1]
volume_of_master = volume_all[0]
volume_of_sounds = volume_all[1]
volume_of_music = volume_all[2]

# загрузка настроек
if os.path.exists("Data/settings.json"):
    with open("Data/settings.json", "r") as s: 
        volume_all = json.load(s)
        volume_of_master = volume_all[0]
        volume_of_sounds = volume_all[1]
        volume_of_music = volume_all[2]

menu_view = main_menu.MainMenu(volume_all)
if __name__ == "__main__":
    window.show_view(menu_view)
    arcade.run()