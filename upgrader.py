from inventory import Inventory
import item
import arcade

class Upgrader():
    def __init__(self, upgrade, area):
        self.upgrade = upgrade
        self.cost = 10
        self.area = area
        
    def update(self, player, inventory: Inventory, keys):
        s_i = inventory.inventory_list[inventory.selected_item]
        
        in_shop = any(arcade.check_for_collision(player, tile) for tile in self.area)
        if not in_shop:
            return
        
        if arcade.key.E in keys and s_i[0] == item.coin and s_i[1] == self.cost:
            inventory.del_item(inventory.selected_item, self.cost)
            self.upgrade += 0.25
            if self.cost % 2:
                self.cost *= 2
            else:
                self.cost += 5