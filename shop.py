from inventory import Inventory
import item
import arcade

class Shop:
    """Магазин"""
    def __init__(self, is_sell: bool, is_buy: bool, amount: int, items, area):
        self.is_sell = is_sell # Продаёт да/нет
        self.is_buy = is_buy # Покупает да/нет
        self.items = items # Список предметов продоваемых/покупаемых
        self.amount = amount # Кол-во
        self.area = area # Список тайлов для арены в которой игрок сможет покупать
        
        # Переменные для задержки кнопок
        self.keys = [
            arcade.key.E, arcade.key.R, arcade.key.T,
            arcade.key.Y, arcade.key.U, arcade.key.I, arcade.key.O
        ]
        
        self.cooldowns = {key: 0.0 for key in self.keys}
        self.cooldown_time = 0.5
        
    def update(self, player, inventory: Inventory, keys, time):
        """Логика магазина"""
        s_i = inventory.inventory_list[inventory.selected_item]
        
        in_shop = any(arcade.check_for_collision(player, tile) for tile in self.area)
        if not in_shop:
            return
        
        if not s_i[0]:
            return
        
        time = time
        
        if self.is_buy and not s_i[0].sellable:
            return

        if self.is_buy:
            for i, shop_item in enumerate(self.items):
                if i >= len(self.keys):
                    break
                key = self.keys[i]

                if key in keys:
                    # Проверка cooldown
                    if time - self.cooldowns[key] < self.cooldown_time:
                        continue  # На перезарядке

                    if s_i[0] == shop_item and s_i[1] >= self.amount:
                        # Добавляем монеты, удаляем предмет
                        inventory.add_item(item.coin, shop_item.price)
                        inventory.del_item(inventory.selected_item, self.amount)
                        self.cooldowns[key] = time  # Обновляем время
                        return

        if self.is_sell:
                for i, shop_item in enumerate(self.items):
                    if i >= len(self.keys):
                        break
                    key = self.keys[i]

                    if key in keys:
                        # Проверка cooldown
                        if time - self.cooldowns[key] < self.cooldown_time:
                            continue

                        if s_i[0] == item.coin and s_i[1] >= shop_item.price:
                            # Продаём shop_item за монеты
                            inventory.add_item(shop_item, self.amount)
                            inventory.del_item(inventory.selected_item, shop_item.price)
                            self.cooldowns[key] = time
                            return