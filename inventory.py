import arcade
import item

class Inventory(arcade.Sprite):
    def __init__(self, x=400, y=32):
        super().__init__(center_x=x, center_y=y, scale=1)
        self.inventory_list = [[None, 0] for _ in range(9)] 
        self.inventory_textures = [arcade.load_texture(f"Data/Images/inventory/inventory{i}.png") for i in range(1, 10)]
        self.selected_item = 0
        self.texture = self.inventory_textures[self.selected_item]
    
    def merge_items(self):
        items_count = {}
        for slot in self.inventory_list:
            item_obj, count = slot
            if item_obj and count > 0:
                if item_obj in items_count:
                    items_count[item_obj] += count
                else:
                    items_count[item_obj] = count

        for i in range(len(self.inventory_list)):
            self.inventory_list[i] = [None, 0]

        for i, (item_obj, total) in enumerate(items_count.items()):
            if i >= len(self.inventory_list):
                break
            self.inventory_list[i] = [item_obj, total]
            item_obj.center_x = 144 + (64 * i)
            item_obj.center_y = self.center_y
        
    def add_item(self, item_obj: item.Item, amount=1):
        for i, (existing_item, count) in enumerate(self.inventory_list):
            if existing_item == item_obj:
                self.inventory_list[i][1] += amount
                self.merge_items()  # Пересортируем и объединяем
                return
            
        for i, (existing_item, count) in enumerate(self.inventory_list):
            if not existing_item:
                self.inventory_list[i] = [item_obj, amount]
                item_obj.center_x = 144 + (64 * i)
                item_obj.center_y = self.center_y
                self.merge_items()  # Гарантируем объединение
                return
    
    def del_item(self, cell=0, amount=1):
        if cell < 0 or cell >= len(self.inventory_list):
            return

        item_obj, count = self.inventory_list[cell]
        if not (item_obj is None) and count >= 0:
            new_count = count - amount
            if new_count <= 0:
                self.inventory_list[cell] = [None, 0]  
            else:
                self.inventory_list[cell][1] = new_count
    
    def clear_cell(self, cell=0):
        self.inventory_list[cell] = [None, 0]
        
    def draw_items(self):
        items_to_draw = arcade.SpriteList()
        for slot in self.inventory_list:
            item_obj, count = slot
            if item_obj and count > 0:
                items_to_draw.append(item_obj)
        items_to_draw.draw()

        
    def update(self, deltatime, keys):
        if arcade.key.NUM_1 in keys:
            self.selected_item = 0
        elif arcade.key.NUM_2 in keys:
            self.selected_item = 1
        elif arcade.key.NUM_3 in keys:
            self.selected_item = 2
        elif arcade.key.NUM_4 in keys:
            self.selected_item = 3
        elif arcade.key.NUM_5 in keys:
            self.selected_item = 4
        elif arcade.key.NUM_6 in keys:
            self.selected_item = 5
        elif arcade.key.NUM_7 in keys:
            self.selected_item = 6
        elif arcade.key.NUM_8 in keys:
            self.selected_item = 7
        elif arcade.key.NUM_9 in keys:
            self.selected_item = 8
        self.texture = self.inventory_textures[self.selected_item]