from inventory import Inventory
import item
import arcade

class Shop:
    def __init__(self, is_sell: bool, is_buy: bool, amount: int, items, area):
        self.is_sell = is_sell
        self.is_buy = is_buy
        self.items = items
        self.amount = amount
        self.area = area
        
        self.keys = [
            arcade.key.E, arcade.key.R, arcade.key.T,
            arcade.key.Y, arcade.key.U, arcade.key.I, arcade.key.O
        ]
        
        self.cooldowns = {key: 0.0 for key in self.keys}
        self.cooldown_time = 0.5
        
    def update(self, player, inventory: Inventory, keys, time):
        s_i = inventory.inventory_list[inventory.selected_item]
        
        in_shop = any(arcade.check_for_collision(player, tile) for tile in self.area)
        if not in_shop:
            return
        
        if not s_i[0]:
            return
        
        current_time = time
        
        if self.is_buy and not s_i[0].sellable:
            return

        if self.is_buy:
            for i, shop_item in enumerate(self.items):
                if i >= len(self.keys):
                    break
                key = self.keys[i]

                if key in keys:
                    # Проверка cooldown
                    if current_time - self.cooldowns[key] < self.cooldown_time:
                        continue  # На перезарядке

                    if s_i[0] == shop_item:
                        # Добавляем монеты, удаляем предмет
                        inventory.add_item(item.coin, shop_item.price)
                        inventory.del_item(inventory.selected_item, self.amount)
                        self.cooldowns[key] = current_time  # Обновляем время
                        return

        if self.is_sell:
                for i, shop_item in enumerate(self.items):
                    if i >= len(self.keys):
                        break
                    key = self.keys[i]

                    if key in keys:
                        # Проверка cooldown
                        if current_time - self.cooldowns[key] < self.cooldown_time:
                            continue

                        if s_i[0] == item.coin:
                            # Продаём shop_item за монеты
                            inventory.add_item(shop_item, self.amount)
                            inventory.del_item(inventory.selected_item, shop_item.price)
                            self.cooldowns[key] = current_time
                            return