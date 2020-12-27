from interfaces.FoodItem import FoodItem

import sqlite3 as db

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class FoodOrderUseCases:

    def retrieve_food_item(self, food_id):
        connection = db.connect('order_items.db')
        connection.row_factory = dict_factory
        with connection:
            c = connection.cursor()
            c.execute("SELECT * FROM FOOD_ITEM WHERE NUMBER = ?", (food_id,))
            result = c.fetchone()
            if result:
                return FoodItem(result['NUMBER'], result['PRICE'], 1, result['DESCRIPTION'], result['CHINESE_DESCRIPTION'])
        return None
