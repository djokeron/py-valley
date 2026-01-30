import arcade


class Window(arcade.Window):
    """Окно всей игры"""
    def __init__(self, width=800, height=600, title="py-valley", full_screen=False):
        super().__init__(width, height, title, fullscreen=full_screen)
        self.windowed_size = (width, height)
        self.pressed_keys = set()
        
        self.full_screen_keyses = (arcade.key.F5, arcade.key.F11)
        self.kill_keyses = (arcade.key.F4, arcade.key.F12)
        
        if full_screen:
            self.set_fullscreen(True)

    
    def on_key_press(self, key, mod):
        if key in self.full_screen_keyses:
                self.toggle_fullscreen()
        
        if key in self.kill_keyses:
                self.close()
        
        if key not in self.pressed_keys:
            self.pressed_keys.add(key)
            
    def on_key_release(self, key, mod):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
            
    def toggle_fullscreen(self):
        """Переключает полноэкранный режим"""
        if self.fullscreen:
            self.set_fullscreen(False)
            width, height = self.windowed_size
            self.set_size(width, height)
            screen_center_x = (self.screen.width - width) // 2
            screen_center_y = (self.screen.height - height) // 2
            self.set_location(screen_center_x, screen_center_y)
        else:
            self.set_fullscreen(True)