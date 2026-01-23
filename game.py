import arcade
from pyglet.graphics import Batch
import pause_menu
from inventory import Inventory
import item
from grad import Grad
from upgrader import Upgrader
from shop import Shop
data = "Data/"
step_sound_1 = arcade.load_sound(f"{data}Sounds/step_1.mp3")
step_sound_2 = arcade.load_sound(f"{data}Sounds/step_2.mp3")

class Player(arcade.Sprite):
    def __init__(self, x=50.75, y=1, volume=1, speed=200):
        super().__init__(center_x=x, center_y=y, scale=1.5)
        self.stand_texture = arcade.load_texture(f"{data}images/Player/Player_stand.png")
        self.texture = self.stand_texture
        
        self.volume = volume
        
        self.walk_speed = speed
        self.walk_frame_index = 0         
        self.walk_timer = 0           
        self.facing_direction = "front"
        self.walk_frame_duration = 0.25
        self.walk_textures = [
            arcade.load_texture(f"{data}images/Player/Player_walk.png"),
            self.stand_texture,
            ]
        
        self.back_walk_textures = [
            arcade.load_texture(f"{data}images/Player/Player_Back_Walk.png"),
            arcade.load_texture(f"{data}images/Player/Player_Back_Stand.png"),
            ]
        
        self.left_walk_textures = [
            arcade.load_texture(f"{data}images/Player/Player_Left_Walk.png"),
            arcade.load_texture(f"{data}images/Player/Player_Left_Stand.png"),
            ]
        
        self.right_walk_textures = [
            arcade.load_texture(f"{data}images/Player/Player_Right_Walk.png"),
            arcade.load_texture(f"{data}images/Player/Player_Right_Stand.png"),
            ]
        
    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        
        self.update_animation(delta_time)

    def update_animation(self, delta_time):
        """Плавная анимация ходьбы с направлением"""
        is_moving = self.change_x != 0 or self.change_y != 0

        if is_moving:
            if self.change_y > 0:
                self.facing_direction = "back"
            elif self.change_y < 0:
                self.facing_direction = "front"
            if self.change_x > 0:
                self.facing_direction = "right"
            elif self.change_x < 0:
                self.facing_direction = "left"

        if is_moving:
            self.walk_timer += delta_time

            if self.walk_timer >= self.walk_frame_duration:
                self.walk_timer = 0
                prev_frame = self.walk_frame_index
                self.walk_frame_index = (self.walk_frame_index + 1) % 2
                
                if self.walk_frame_index != prev_frame:
                    if self.walk_frame_index == 0:
                        arcade.play_sound(step_sound_1, self.volume)
                    else:
                        arcade.play_sound(step_sound_2, self.volume)

            if self.facing_direction == "front":
                self.texture = self.walk_textures[self.walk_frame_index]
            elif self.facing_direction == "back":
                self.texture = self.back_walk_textures[self.walk_frame_index]
            elif self.facing_direction == "left":
                self.texture = self.left_walk_textures[self.walk_frame_index]
            elif self.facing_direction == "right":
                self.texture = self.right_walk_textures[self.walk_frame_index]
        else:
            self.walk_timer = 0  
            if self.facing_direction == "front":
                self.texture = self.stand_texture
            elif self.facing_direction == "back":
                self.texture = self.back_walk_textures[1]
            elif self.facing_direction == "left":
                self.texture = self.left_walk_textures[1]
            elif self.facing_direction == "right":
                self.texture = self.right_walk_textures[1]


class Game(arcade.View):
    def __init__(self, loaded_data=None, volume=[1, 1, 1]):
        super().__init__()
        
        self.volume = volume
        
        player = Player(x=896, y=832, volume=(self.volume[1] * self.volume[0]))
        self.player_list = arcade.SpriteList()
        self.player_list.append(player)
        
        self.pressed_keys = set()
        
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        
        self.world_width = 800
        self.world_height = 600
        
        self.location1 = f"{data}Map/valley.tmx"
        self.loc_map1 = arcade.load_tilemap(self.location1, scaling=1)
        self.wall_list = self.loc_map1.sprite_lists["hat"]
        self.wall_list2 = self.loc_map1.sprite_lists["zab2"]
        self.wall_list3 = self.loc_map1.sprite_lists["zab3"]
        self.collision_list = self.loc_map1.sprite_lists["coll"]
        self.ground_list = self.loc_map1.sprite_lists["ground"]
        
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_list[0], self.collision_list
        )
        
        self.upgrade = 1.25

        self.game_globaltime = 0
        
        self.game_hours = 9   
        self.game_minutes = 0
        self.game_seconds = 0.0 
        
        # Ускорение времени: 60x (1 реальная секунда = 1 игровая минута)
        self.time_speedup = 60.0
        
        self.list_of_grads = []
        for i in range(1, 9):
            listi = []
            for layer_name, sprite_list in self.loc_map1.sprite_lists.items():
                if f"grad_{i}" in layer_name:
                    listi.append((layer_name, sprite_list))
            if listi:
                self.list_of_grads.append(Grad(listi))    
        
        self.shop_1 = Shop(False, True, 1, (item.carrot, item.hren, item.ginger, item.beet, item.potato, item.tomato, item.cucumber), self.loc_map1.sprite_lists["shop_point_1"]) 
        self.shop_2 = Shop(True, False, 1, (item.carrot_seed, item.hren_seed, item.ginger_seed, item.beet_seed, item.potato, item.tomato_seed, item.cucumber_seed), self.loc_map1.sprite_lists["shop_point_2"]) 
        self.shop_3 = Upgrader(self.loc_map1.sprite_lists["shop_point_3"])             
        
        self.inventory = Inventory()
        self.inventory_draw = arcade.SpriteList()
        self.inventory_draw.append(self.inventory)
        if not loaded_data:
            self.inventory.add_item(item.carrot_seed, 1)
    
        if loaded_data:
            self.player_list[0].center_x, self.player_list[0].center_y = loaded_data[0], loaded_data[1]
            
            self.game_hours = loaded_data[2]
            self.game_minutes = loaded_data[3]
            self.game_globaltime = loaded_data[4]
            
            for items in loaded_data[5]:
                self.inventory.add_item(item.item_dict[items[0]], items[1])
                
            lof = self.list_of_grads
            for num, grad in enumerate(loaded_data[6]):
                lof[num].active = grad[0]
                lof[num].vegetable = grad[1]
                lof[num].washed = grad[2]
                lof[num].stage = grad[3]
                lof[num].cycle = grad[4]
                lof[num].redused = grad[5]
                lof[num].growth_time = grad[6]
    
        self.save_data = []
        self.batch = Batch()

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        
        self.ground_list.draw()
        
        for grad in self.list_of_grads:
            grad.draw()
            
        self.wall_list.draw()
        
        self.wall_list3.draw()
        
        self.player_list.draw()
        
        self.wall_list2.draw()
        
        self.gui_camera.use()
        
        self.batch.draw()
        
        self.inventory_draw.draw()
        self.inventory.draw_items()
        
    def on_update(self, delta_time):
        self.game_globaltime += delta_time
        
        self.inventory.update(deltatime=delta_time, keys=self.pressed_keys)
        s_i = self.inventory.inventory_list[self.inventory.selected_item]
        
        self.player_list[0].change_x = 0
        self.player_list[0].change_y = 0
        
        if arcade.key.UP in self.pressed_keys or arcade.key.W in self.pressed_keys:
            self.player_list[0].change_y = 200 * delta_time
            
        elif arcade.key.DOWN in self.pressed_keys or arcade.key.S in self.pressed_keys:
            self.player_list[0].change_y = -200 * delta_time

        if arcade.key.RIGHT in self.pressed_keys or arcade.key.D in self.pressed_keys:
            self.player_list[0].change_x = 200 * delta_time
            
        elif arcade.key.LEFT in self.pressed_keys or arcade.key.A in self.pressed_keys:
            self.player_list[0].change_x = -200 * delta_time
        
        self.player_list[0].update(delta_time)
        
        self.physics_engine.update()
        
        position = (
            self.player_list[0].center_x,
            self.player_list[0].center_y
        )
        
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            position,
            0.14,
        ) 
                
        for grad in self.list_of_grads:
            grad.update(self.player_list[0], self.inventory, self.pressed_keys, self.game_globaltime, self.volume[1] * self.volume[0])
            if grad.active and grad.vegetable:
                grad.update_growth(delta_time=delta_time, inventory=self.inventory, upgrade=self.upgrade, volume=self.volume[1] * self.volume[0])
        
        self.shop_1.update(self.player_list[0], self.inventory, self.pressed_keys, self.game_globaltime)    
        self.shop_2.update(self.player_list[0], self.inventory, self.pressed_keys, self.game_globaltime)
        self.upgrade = self.shop_3.update(self.player_list[0], self.inventory, self.pressed_keys, self.upgrade)
        
        self.game_seconds += delta_time * self.time_speedup
        
        while self.game_seconds >= 60.0:
            self.game_seconds -= 60.0
            self.game_minutes += 1
            
        while self.game_minutes >= 60:
            self.game_minutes -= 60
            self.game_hours += 1

        self.game_hours %= 24
        
        self.time_text = arcade.Text(f"Время: {self.game_hours:02d}:{self.game_minutes:02d}",
        x=10,
        y=self.window.height - 30,
        color=arcade.color.WHITE,
        font_size=20,
        bold=True,
        batch=self.batch)
        
        if s_i[0]:
            self.item_text = arcade.Text(f"""Выбранный предмет:\n{s_i[0].name}\nКол-во: {s_i[1]}\nЦена: {s_i[0].price}""",
            x=10,
            y=self.window.height - 50,
            color=arcade.color.WHITE,
            font_size=20,
            bold=True,
            width=300,
            multiline=True,
            batch=self.batch)
        else:
            self.item_text = arcade.Text(f"""Выбранный предмет:\nНет""",
            x=10,
            y=self.window.height - 50,
            color=arcade.color.WHITE,
            font_size=20,
            bold=True,
            width=300,
            multiline=True,
            batch=self.batch)
        
        self.hint_text = arcade.Text(f"""""",
            x=self.window.width - 200,
            y=self.window.height - 30,
            color=arcade.color.WHITE,
            font_size=20,
            bold=True,
            width=200,
            multiline=True,
            batch=self.batch)
            
        for tile in self.loc_map1.sprite_lists["text_shop_1"]:
            if arcade.check_for_collision(self.player_list[0], tile):
                self.hint_text.text = """Продать:\nE: Морковь\nR: Хрен\nT: Имбирь\nY: Свеклу\nU: Картошку\nI: Помидор\nO: Огурец"""

        
        for tile in self.loc_map1.sprite_lists["text_shop_2"]:
            if arcade.check_for_collision(self.player_list[0], tile):
                self.hint_text.text = """Купить семена:\nE: Моркови, 1 мон.\nR: Хрена, 4 мон.\nT: Имбиря, 8 мон.\nY: Свеклы, 8 мон.\nU: Картошку, 6 мон.\nI: Помидоры, 32 мон.\nO: Огурца, 32 мон."""

        
        for tile in self.loc_map1.sprite_lists["text_shop_3"]:
            if arcade.check_for_collision(self.player_list[0], tile):
                self.hint_text.text = f"""Купить Улучшение:\nЦена: {self.shop_3.cost}\nЭффективность: {self.upgrade + 0.25}"""

                

    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.ESCAPE:
            saving_inv = []
            
            for items in self.inventory.inventory_list:
                if items[0]:
                    saving_inv.append((items[0].id, items[1]))
            saving_grads = []
            
            for grad in self.list_of_grads:
                saving_grads.append((grad.active, 
                                     grad.vegetable, 
                                     grad.washed,
                                     grad.stage,
                                     grad.cycle,
                                     grad.redused,
                                     grad.growth_timer))
                
            self.save_data = (self.player_list[0].center_x,
            self.player_list[0].center_y,
            self.game_hours,  
            self.game_minutes,
            self.game_globaltime,
            saving_inv,
            saving_grads)
            
            self.window.show_view(pause_menu.PauseMenu(self, self.volume))
        if key not in self.pressed_keys:
            self.pressed_keys.add(key)
            
    def on_key_release(self, key, modifiers):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
            
    def on_show_view(self):
        """Вызывается, когда вид показывается (например, при переходе)"""
        # Загружаем и запускаем музыку
        self.background_music = arcade.load_sound("Data/sounds/music.wav", True)
        self.current_song = arcade.play_sound(self.background_music, volume=(self.volume[2] * self.volume[0]), loop=True)
        
    def on_hide_view(self):
        """Останавливаем музыку, когда уходим с экрана (например, в паузу)"""
        if self.current_song:
            arcade.stop_sound(self.current_song)
            self.current_song = None


class Tutorial(arcade.View):
    def __init__(self, volume, menu):
        super().__init__()
        self.menu = menu
        self.volume = volume
        
        self.pressed_keys = set()
        
        player = Player(x=256, y=1024, volume=self.volume[1]*self.volume[0])
        self.player_list = arcade.SpriteList()
        self.player_list.append(player)
        
        self.location1 = f"{data}Map/tutorial.tmx"
        self.loc_map1 = arcade.load_tilemap(self.location1, scaling=1)
        self.wall_list = self.loc_map1.sprite_lists["zabor"] 
        self.shop_list1 = self.loc_map1.sprite_lists["shop_1"]
        self.shop_list2 = self.loc_map1.sprite_lists["shop_2"]
        self.wall_list2 = self.loc_map1.sprite_lists["zab2"]

        self.collision_list = self.loc_map1.sprite_lists["coll"]
        self.ground_list = self.loc_map1.sprite_lists["ground"]
        
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        
        self.upgrade = 1.25

        self.game_globaltime = 0
        
        self.inventory = Inventory()
        self.inventory_draw = arcade.SpriteList()
        self.inventory_draw.append(self.inventory)
        self.inventory.add_item(item.carrot_seed, 1)
        
        self.game_hours = 9   
        self.game_minutes = 0
        self.game_seconds = 0.0 
        
        # Ускорение времени: 60x (1 реальная секунда = 1 игровая минута)
        self.time_speedup = 60.0
        
        self.list_of_grads = []
        for i in range(1, 9):
            listi = []
            for layer_name, sprite_list in self.loc_map1.sprite_lists.items():
                if f"grad_{i}" in layer_name:
                    listi.append((layer_name, sprite_list))
            if listi:
                self.list_of_grads.append(Grad(listi))    
        
        self.shop_1 = Shop(False, True, 1, (item.carrot, item.hren, item.ginger, item.beet, item.potato, item.tomato, item.cucumber), self.loc_map1.sprite_lists["shop_point_1"]) 
        self.shop_2 = Shop(True, False, 1, (item.carrot_seed, item.hren_seed, item.ginger_seed, item.beet_seed, item.potato, item.tomato_seed, item.cucumber_seed), self.loc_map1.sprite_lists["shop_point_3"]) 
        self.shop_3 = Upgrader(self.loc_map1.sprite_lists["shop_point_2"])
        
        self.batch = Batch()
         
        self.hint_text = arcade.Text(f"""Подсказка""",
            x= self.window.width - 200,
            y = self.window.height - 30,
            color=arcade.color.WHITE,
            font_size=20,
            bold=True,
            width=200,
            multiline=True,
            batch=self.batch)
        
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_list[0], self.collision_list
        )
        

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        
        self.ground_list.draw()
        
        for grad in self.list_of_grads:
            grad.draw()
            
        self.wall_list.draw()
        
        self.wall_list2.draw()
        
        self.shop_list2.draw()
        
        self.player_list.draw()
        
        self.shop_list1.draw()
        
        self.gui_camera.use()
        
        self.batch.draw()
        
        self.inventory_draw.draw()
        self.inventory.draw_items()
        
    def on_update(self, delta_time):
        self.game_globaltime += delta_time
        
        self.inventory.update(deltatime=delta_time, keys=self.pressed_keys)
        s_i = self.inventory.inventory_list[self.inventory.selected_item]
        
        self.player_list[0].change_x = 0
        self.player_list[0].change_y = 0
        
        if arcade.key.UP in self.pressed_keys or arcade.key.W in self.pressed_keys:
            self.player_list[0].change_y = 200 * delta_time
            
        elif arcade.key.DOWN in self.pressed_keys or arcade.key.S in self.pressed_keys:
            self.player_list[0].change_y = -200 * delta_time

        if arcade.key.RIGHT in self.pressed_keys or arcade.key.D in self.pressed_keys:
            self.player_list[0].change_x = 200 * delta_time
            
        elif arcade.key.LEFT in self.pressed_keys or arcade.key.A in self.pressed_keys:
            self.player_list[0].change_x = -200 * delta_time
        
        self.player_list[0].update(delta_time)
        
        self.physics_engine.update()
        
        position = (
            self.player_list[0].center_x,
            self.player_list[0].center_y
        )
        
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            position,
            0.14,
        ) 
                
        for grad in self.list_of_grads:
            grad.update(self.player_list[0], self.inventory, self.pressed_keys, self.game_globaltime, self.volume[1] * self.volume[0])
            grad.update_growth(delta_time=delta_time, inventory=self.inventory, upgrade=self.upgrade, volume=self.volume)
        
        self.shop_1.update(self.player_list[0], self.inventory, self.pressed_keys, self.game_globaltime)    
        self.shop_2.update(self.player_list[0], self.inventory, self.pressed_keys, self.game_globaltime)
        self.upgrade = self.shop_3.update(self.player_list[0], self.inventory, self.pressed_keys, self.upgrade)
        
        self.game_seconds += delta_time * self.time_speedup
        
        while self.game_seconds >= 60.0:
            self.game_seconds -= 60.0
            self.game_minutes += 1
            
        while self.game_minutes >= 60:
            self.game_minutes -= 60
            self.game_hours += 1

        self.game_hours %= 24
        
        self.time_text = arcade.Text(f"Время: {self.game_hours:02d}:{self.game_minutes:02d}",
        x=10,
        y=self.window.height - 30,
        color=arcade.color.WHITE,
        font_size=20,
        bold=True,
        batch=self.batch)
        
        if s_i[0]:
            self.item_text = arcade.Text(f"""Выбранный предмет:\n{s_i[0].name}\nКол-во: {s_i[1]}\nЦена: {s_i[0].price}""",
            x=10,
            y=self.window.height - 50,
            color=arcade.color.WHITE,
            font_size=20,
            bold=True,
            width=300,
            multiline=True,
            batch=self.batch)
        else:
            self.item_text = arcade.Text(f"""Выбранный предмет:\nНет""",
            x=10,
            y=self.window.height - 50,
            color=arcade.color.WHITE,
            font_size=20,
            bold=True,
            width=300,
            multiline=True,
            batch=self.batch)
        
        for tile in self.loc_map1.sprite_lists["text_1"]:
            if arcade.check_for_collision(self.player_list[0], tile):
                self.hint_text.text = """Подсказка:\nХодьба на WASD или стрелки\nПоменять выбранный предмет в инвентаре\nна цыфры 1-9"""
    
        for tile in self.loc_map1.sprite_lists["text_2"]:
            if arcade.check_for_collision(self.player_list[0], tile):
                self.hint_text.text = """Подсказка:\nВыбери семена,\nВстань на грядку\nи два раза нажми E\nЧтобы полить нажми R\nДля большей информации нажми E или R вне грядки"""
                if arcade.key.E in self.pressed_keys:
                    self.hint_text.text = """Подсказка:\nЧто бы морковка вырасла придётся подождать 3 внутриигровых часа полив уменьшает количество времяни"""
                if arcade.key.R in self.pressed_keys:
                    self.hint_text.text = """Подсказка:\nМожно сажать только семена и картошку.\nУ каждого растения разное время выращивания"""
                
        for tile in self.loc_map1.sprite_lists["text_3"]:
            if arcade.check_for_collision(self.player_list[0], tile):
                self.hint_text.text = """Подсказка:\nВ Магазинах можно\nпокупать или продавать тебе предметы\nподойди к одному из магазинов для большей информации\nИли нажми на E для ещё информации"""
                if arcade.key.E in self.pressed_keys:
                    self.hint_text.text = """Подсказка:\nЧтобы отдать цену или предмет нужно переключить инвентарь на ячейку с этим предметом"""
                
        for tile in self.loc_map1.sprite_lists["text_3_1"]:
            if arcade.check_for_collision(self.player_list[0], tile):
                self.hint_text.text = """Подсказка:\nЭтот магазин покупает у тебя овощи на кнопках с E до O на клвиатуре, ты продаёшь разные овощи, Семена(Кроме картошки) продавать нельзя"""
                if arcade.key.E in self.pressed_keys:
                        self.hint_text.text = """Подсказка:\nЗа продажу ты получаешь монеты, их можно потратить на улучшение полива и на семена"""
               
        for tile in self.loc_map1.sprite_lists["text_3_2"]:
            if arcade.check_for_collision(self.player_list[0], tile):
                self.hint_text.text = """Подсказка:\nЭтот магазин улучшает твой полив за монеты, с каждым улучшением цена возрастает"""
                
        for tile in self.loc_map1.sprite_lists["text_3_3"]:
            if arcade.check_for_collision(self.player_list[0], tile):
                self.hint_text.text = """Подсказка:\nЭтот магазин продаёт тебе семена с кнопки Е до O на клавиатуре продаёт тебе разные семена и картошку""" 
        
        for tile in self.loc_map1.sprite_lists["text_4"]:
            if arcade.check_for_collision(self.player_list[0], tile):
                self.hint_text.text = """Подсказка:\nНа кнопку ESC выходи""" 
                
               
    def on_key_press(self, key, modifiers):  
        if key == arcade.key.ESCAPE:
            self.menu.manager.enable()
            self.window.show_view(self.menu)
        if key not in self.pressed_keys:
            self.pressed_keys.add(key)
    
    def on_key_release(self, key, modifiers):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
            
    def on_show_view(self):
        """Вызывается, когда вид показывается (например, при переходе)"""
        # Загружаем и запускаем музыку
        self.background_music = arcade.load_sound("Data/sounds/music.wav", True)
        self.current_song = arcade.play_sound(self.background_music, volume=(self.volume[2] * self.volume[0]), loop=True)
        
    def on_hide_view(self):
        """Останавливаем музыку, когда уходим с экрана (например, в паузу)"""
        if self.current_song:
            arcade.stop_sound(self.current_song)
            self.current_song = None