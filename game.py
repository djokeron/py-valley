import arcade
import pause_menu


class Player(arcade.Sprite):
    def __init__(self, x=50.75, y=1):
        super().__init__(center_x=x, center_y=y, scale=1.5)
        self.stand_texture = arcade.load_texture("images/Player/Player_stand.png")
        self.texture = self.stand_texture
        self.walk_speed = 200
        self.walk_frame_index = 0         
        self.walk_timer = 0           
        self.facing_direction = "front"
        self.walk_frame_duration = 0.25
        self.walk_textures = [
            arcade.load_texture("images/Player/Player_walk.png"),
            self.stand_texture,
            ]
        
        self.back_walk_textures = [
            arcade.load_texture("images/Player/Player_Back_Walk.png"),
            arcade.load_texture("images/Player/Player_Back_Stand.png"),
            ]
        
        self.left_walk_textures = [
            arcade.load_texture("images/Player/Player_Left_Walk.png"),
            arcade.load_texture("images/Player/Player_Left_Stand.png"),
            ]
        
        self.right_walk_textures = [
            arcade.load_texture("images/Player/Player_Right_Walk.png"),
            arcade.load_texture("images/Player/Player_Right_Stand.png"),
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
                self.walk_frame_index = (self.walk_frame_index + 1) % 2

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
    def __init__(self):
        super().__init__()
        player = Player(x=832, y=448)
        self.player_list = arcade.SpriteList()
        self.player_list.append(player)
        self.pressed_keys = set()
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        self.world_width = 800
        self.world_height = 600
        self.location1 = "map1.tmx"
        self.loc_map1 = arcade.load_tilemap(self.location1, scaling=1)
        self.wall_list = self.loc_map1.sprite_lists["hat"]
        self.wall_list2 = self.loc_map1.sprite_lists["zab2"]
        self.collision_list = self.loc_map1.sprite_lists["coll"]
        self.ground_list = self.loc_map1.sprite_lists["ground"]
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_list[0], self.collision_list
        )
   
    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.ground_list.draw()
        self.wall_list2.draw()
        self.wall_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
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
        
            
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            pause_view = pause_menu.PauseMenu() 
            self.window.show_view(pause_view)
        if key not in self.pressed_keys:
            self.pressed_keys.add(key)
            
    def on_key_release(self, key, modifiers):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)