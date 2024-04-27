""" A Bunch of ultity functions to interface with DB"""

from interfaces.FoodItem import FoodItem
import sqlite3 as db
from db_variables import CHOWS_MAIN_DB

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DuplicateFoodException(Exception):
    def __init__(self, message):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

class DbFoodItems:
  
    @staticmethod
    def retrieve_food_items_by_id(sub_id):
        connection = db.connect(CHOWS_MAIN_DB)
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
    def retrieve_food_items_by_description(text):
        connection = db.connect(CHOWS_MAIN_DB)
        connection.row_factory = dict_factory
        food_items = []
        with connection:
            c = connection.cursor()
            sql_query_string = "SELECT * FROM FOOD_ITEM WHERE DESCRIPTION LIKE '%'||?||'%'"
            c.execute(sql_query_string, (text,))
            rows = c.fetchall()
            for row in rows:
                food_items.append(FoodItem(row['ITEM_ID'], float(row['PRICE']), 1, row['DESCRIPTION'], row['DESCRIPTION_CHINESE']))
        return food_items


    @staticmethod
    def create_food_item(id, description, description_chinese, price):
        """ Creates a row if id has not been created."""
        connection = db.connect(CHOWS_MAIN_DB)
        connection.row_factory = dict_factory

        with connection:
            c = connection.cursor()
            try:
                insert_new_food_item = (id, description, description_chinese, price)
                c.execute("""   INSERT INTO FOOD_ITEM (ITEM_ID, DESCRIPTION, DESCRIPTION_CHINESE, PRICE) 
                                VALUES (?, ?, ?, ?) """, 
                            insert_new_food_item)

            except db.IntegrityError as e:
                raise e
            connection.commit()
            