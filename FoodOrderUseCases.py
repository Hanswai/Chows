from interfaces.FoodItem import FoodItem
import sqlite3 as db
from enum import Enum
from datetime import datetime
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class MethodToArrive(Enum):
    COLLECTION = 1
    DELIVERY = 2


class FoodOrder:
    def __init__(self):
        self.retreived_food_items = []
        self.ordered_food_items = []

    def reset(self):
        self.retreived_food_items.clear()
        self.ordered_food_items.clear()

    def add_to_food_order(self, food_item):
        if food_item is None:
            print("Why are you giving me a None?")
            return
        result = next((x for x in self.ordered_food_items if x.item_number == food_item.item_number), None)
        if result:
            result.quantity += 1
        else:
            self.ordered_food_items.append(food_item)                
    
    def get_all_food_items(self):
        return self.ordered_food_items
    
    def get_total_price(self):
        sum = 0
        for i in self.ordered_food_items:
            sum += i.get_total_price()
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

    def save_order_to_db(self):
        connection = db.connect('chows_db.db')
        connection.row_factory = dict_factory
        with connection:
            c = connection.cursor()
            insert_db = (datetime.now(), 
                        "COLLECTION", 
                        "123ABC", 
                        str(self.get_total_price()))
            c.execute("""   INSERT INTO ORDER_DETAILS (DATE_RECEIVED, ORDER_TYPE, CUSTOMER_ID, TOTAL_PRICE) 
                            VALUES (?, ?, ?, ?) """, 
                        insert_db)
        connection.commit()
        connection.close()

    def retrieve_food_item(self, food_id):
        connection = db.connect('chows_db.db')
        connection.row_factory = dict_factory
        with connection:
            c = connection.cursor()
            c.execute("SELECT * FROM FOOD_ITEM WHERE ITEM_ID = ?", (food_id,))
            result = c.fetchone()
            if result:
                food_item = FoodItem(result['ITEM_ID'], float(result['PRICE']), 1, result['DESCRIPTION'], result['DESCRIPTION_CHINESE'])
                self.retreived_food_items.append(food_item)
                return food_item
        return None
