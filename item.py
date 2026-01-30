import arcade

# Словарь циклов
cycles = {"Carrot": 180,
          "Hren": 240,
          "Beet": 420,
          "Ginger": 240,
          "Tomato": 840,
          "Cucumber": 1440,
          "Potat": 330}


class Item(arcade.Sprite):
    """Предмет структура с тектурой"""
    def __init__(self, id: str, item_name="item", x=0, y=0, item_type="item", texture=None, price=0, sellable=False):
        super().__init__(path_or_texture=texture,center_x=x, center_y=y, scale=1)
        self.price = price # Цена
        self.sellable = sellable # Продаваемый да/нет
        self.type = item_type # Тип предмета
        self.id = id # Индетификатор объекта
        self.name = item_name # Имя объекта
        # Если объект семена то добавляется к нему пораметр cycle из словаря
        if item_type == "seed":
            self.cycle_of_plant = cycles[id[:id.rfind('_')]]
 
# Все предметы в игре       
carrot = Item("Carrot", "Морковь", texture=arcade.load_texture("Data/Images/Vegetables/Carrot.png"), price=2, sellable=True)
carrot_seed = Item("Carrot_seed", "Семена моркови", item_type="seed", texture=arcade.load_texture("Data/Images/Vegetables/CarrotSeed.png"), price=1, sellable=False)
coin = Item("Сoin", "Монета", item_type="coin", texture=arcade.load_texture("Data/Images/coin.png"), sellable=False)
hren = Item("Hren", "Хрен", texture=arcade.load_texture("Data/Images/Vegetables/Hren.png"), price=6, sellable=True)
hren_seed = Item("Hren_seed", "Семена хрена", item_type="seed", texture=arcade.load_texture("Data/Images/Vegetables/HrenSeed.png"), price=4, sellable=False)
beet = Item("Beet", "Свёкла", texture=arcade.load_texture("Data/Images/Vegetables/Beet.png"), price=12, sellable=True)
beet_seed = Item("Beet_seed", "Семена свёклы", item_type="seed", texture=arcade.load_texture("Data/Images/Vegetables/BeetSeed.png"), price=8, sellable=False)
ginger = Item("Ginger", "Имбирь", texture=arcade.load_texture("Data/Images/Vegetables/Ginger.png"), price=10, sellable=True)
ginger_seed = Item("Ginger_seed", "Семена имбиря", item_type="seed", texture=arcade.load_texture("Data/Images/Vegetables/GingerSeed.png"), price=8, sellable=False)
tomato = Item("Tomato", "Помидор", texture=arcade.load_texture("Data/Images/Vegetables/Tomato.png"), price=47, sellable=True)
tomato_seed = Item("Tomato_seed", "Семена помидоры", item_type="seed", texture=arcade.load_texture("Data/Images/Vegetables/TomatoSeed.png"), price=32, sellable=False)
cucumber = Item("Cucumber", "Огурец", texture=arcade.load_texture("Data/Images/Vegetables/Cucumber.png"), price=250, sellable=True)
cucumber_seed = Item("Cucumber_seed", "Семена моркови", item_type="seed", texture=arcade.load_texture("Data/Images/Vegetables/CucumberSeed.png"), price=32, sellable=False)
potato = Item("Potato", "Картошка", item_type="seed", texture=arcade.load_texture("Data/Images/Vegetables/Potato.png"), price=6, sellable=True)


# Словарь предметов
item_dict = {
    carrot.id: carrot,
    carrot_seed.id: carrot_seed,
    coin.id: coin,
    hren.id: hren,
    beet.id: beet,
    beet_seed.id: beet_seed,
    hren_seed.id: hren_seed,
    ginger.id: ginger,
    tomato.id: tomato,
    cucumber.id: cucumber,
    potato.id: potato,
    cucumber_seed.id: cucumber_seed,
    tomato_seed.id: tomato_seed,
    ginger_seed.id: ginger_seed,
}