from inventory import Inventory
from item import item_dict
from random import randint
import arcade
seeding = arcade.load_sound("Data/Sounds/seeding.mp3", True)


class Grad():
    def __init__(self, list_of_layers):
        self.active = False
        self.vegetable = ""
        self.now_texture = None
        self.active_texture = list_of_layers[0][1]
        self.washed_texture = list_of_layers[1][1]
        self.vegetable_textures = [i[1] for i in list_of_layers if i[0][:i[0].rfind("carrot") + 1]]
        self.washed = False
        self.stage = 0
        self.cycle = 0
        self.redused = False
        self.growth_timer = 0.0
        
        self.last_e_press = 0  # Время последнего нажатия E
        self.last_r_press = 0  # Время последнего нажатия R
        self.cooldown = 0.25
        
    def draw(self):
        if self.active:
            self.now_texture = self.active_texture
        if self.active and self.washed:
            self.now_texture = self.washed_texture
        if self.vegetable:
            if (not self.washed) and self.stage == 1:
                self.now_texture = self.vegetable_textures[0]
            elif self.washed and self.stage == 1:
                self.now_texture = self.vegetable_textures[3]
            elif (not self.washed) and self.stage == 2:
                self.now_texture = self.vegetable_textures[1]
            elif self.washed and self.stage == 2:
                self.now_texture = self.vegetable_textures[4]
            elif (not self.washed) and self.stage == 3:
                self.now_texture = self.vegetable_textures[2]
            elif self.washed and self.stage == 3:
                self.now_texture = self.vegetable_textures[5]
        if self.now_texture:
            self.now_texture.draw()
    
    def update(self, player, inventory: Inventory, keys, time, volume):
        s_i = inventory.inventory_list[inventory.selected_item]
        if not self.active:
            for tile in self.active_texture:
                if arcade.check_for_collision(player, tile):
                    if arcade.key.E in keys:
                        if time - self.last_e_press >= self.cooldown:
                            self.active = True
                            self.now_texture = self.active_texture
                            self.last_e_press = time
                
        
        else:
            for tile in self.active_texture:
                if arcade.check_for_collision(player, tile):
                    if arcade.key.R in keys:
                        if time - self.last_r_press >= self.cooldown:
                            self.washed = True
                            arcade.play_sound(arcade.load_sound("Data/Sounds/wash.mp3", True), volume)
                            self.last_r_press = time
                    if arcade.key.E in keys and s_i[0] and s_i[0].type == "seed" and s_i[1] >= 1:
                        if time - self.last_e_press >= self.cooldown:
                            self.vegetable = s_i[0].id[:s_i[0].id.rfind('_')]
                            self.cycle = s_i[0].cycle_of_plant
                            self.stage = 1
                            arcade.play_sound(seeding, volume)
                            inventory.del_item(inventory.selected_item, 1)
                            self.last_e_press = time

        
    def update_growth(self, delta_time, inventory: Inventory, upgrade: float, volume):
        
        
        if self.stage == 3:
            self.growth_timer = 0.0
            if not self.vegetable == "Potat":
                inventory.add_item(item_dict[self.vegetable], randint(2, 5))
            else:
                inventory.add_item(item_dict["Potato"], randint(2, 5))
            self.vegetable = ""
            self.cycle = 0
            self.stage = 0
            arcade.play_sound(seeding, volume)
            self.washed = False
            self.redused = False
            return
        
        if self.washed and not self.redused:
            self.cycle /= upgrade
            self.redused = True
        
        self.growth_timer += delta_time  

        # Пороги роста (в секундах)
        stage_1_to_2 = self.cycle * (1/3) 
        stage_2_to_3 = self.cycle * (2/3)  

        if self.stage == 1 and self.growth_timer >= stage_1_to_2:
            self.stage = 2
        elif self.stage == 2 and self.growth_timer >= stage_2_to_3:
            self.stage = 3
       
