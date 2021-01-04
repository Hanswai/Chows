""" A Bunch of ultity functions to interface with DB"""

from interfaces.FoodItem import FoodItem
import sqlite3 as db

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DbFoodItems:
  
    @staticmethod
    def retrieve_food_items_by_id(sub_id):
        connection = db.connect('chows_db.db')
        connection.row_factory = dict_factory
        food_items = []
        with connection:
            c = connection.cursor()
            sql_query_string = "SELECT * FROM FOOD_ITEM WHERE ITEM_ID LIKE ?||'%'"
            c.execute(sql_query_string, (sub_id,))
            rows = c.fetchall()
            for row in rows:
                food_items.append(FoodItem(row['ITEM_ID'], float(row['PRICE']), 1, row['DESCRIPTION'], row['DESCRIPTION_CHINESE']))
        return food_items

    @staticmethod
    def retrieve_food_items_by_description(sub_id):
        connection = db.connect('chows_db.db')
        connection.row_factory = dict_factory
        food_items = []
        with connection:
            c = connection.cursor()
            sql_query_string = "SELECT * FROM FOOD_ITEM WHERE DESCRIPTION LIKE '%'||?||'%'"
            c.execute(sql_query_string, (sub_id,))
            rows = c.fetchall()
            for row in rows:
                food_items.append(FoodItem(row['ITEM_ID'], float(row['PRICE']), 1, row['DESCRIPTION'], row['DESCRIPTION_CHINESE']))
        return food_items

