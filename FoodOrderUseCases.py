from interfaces.FoodItem import FoodItem

import sqlite3 as db

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class FoodOrder:
    def __init__(self):
        self.retreived_food_items = []
        self.ordered_food_items = []

    def reset(self):
        self.retreived_food_items.clear()
        self.ordered_food_items = []

    def add_to_food_order(self, food_item):
        # If no duplicate retrieve from db and then add?
        if food_item is None:
            print("Why are you giving me a None?")
            return
            
        if len(self.ordered_food_items) > 0:
            result = next((x for x in self.ordered_food_items if x.item_number == food_item.item_number), None)
            if result:
                result.quantity += 1
        self.ordered_food_items.append(food_item)
        print(self.get_total_price())
    
    def get_total_price(self):
        sum = 0
        for i in self.ordered_food_items:
            sum += float(i.price)
        return sum
    
    def get_food_item(self, food_id):
        if food_id:
            # check to see if I have retrieved it already
            if len(self.retreived_food_items) > 0:
                result = next((x for x in self.retreived_food_items if x.item_number == food_id), None)
                if result:
                    return result
            # Otherwise retrieve from db.
            return self.retrieve_food_item(food_id)

    def retrieve_food_item(self, food_id):
        connection = db.connect('order_items.db')
        connection.row_factory = dict_factory
        with connection:
            c = connection.cursor()
            c.execute("SELECT * FROM FOOD_ITEM WHERE NUMBER = ?", (food_id,))
            result = c.fetchone()
            if result:
                food_item = FoodItem(result['NUMBER'], result['PRICE'], 1, result['DESCRIPTION'], result['CHINESE_DESCRIPTION'])
                self.retreived_food_items.append(food_item)
                return food_item
        return None
