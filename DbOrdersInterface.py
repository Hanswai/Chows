""" A Bunch of ultity functions to interface with DB"""

from interfaces.SummaryFoodItem import SummaryFoodItem
from FoodOrderUseCases import FoodOrder
import sqlite3 as db
from enum import Enum
from datetime import datetime



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DbOrders:
    @staticmethod
    def retrieve_total_price_by_date(date):
        connection = db.connect('chows_db.db')
        connection.row_factory = dict_factory
        sum = 0
        with connection:
            c = connection.cursor()
            c.execute("SELECT TOTAL_PRICE FROM ORDER_DETAILS WHERE DATE_RECEIVED = date(?)", (date,))
            rows = c.fetchall()
            for row in rows:                
                sum += float(row['TOTAL_PRICE'])
            return sum
        return 0
    
    @staticmethod
    def retrieve_food_items_and_qty_by_date(date):
        connection = db.connect('chows_db.db')
        connection.row_factory = dict_factory
        food_item_id_to_qty = {}
        with connection:
            c = connection.cursor()
            sql_query_string = """            
                                SELECT 
                                    oi.FOOD_ITEM_ID, 
                                    oi.QUANTITY, 
                                    fi.DESCRIPTION,
                                    fi.DESCRIPTION_CHINESE
                                FROM ORDER_DETAILS od 
                                INNER JOIN ORDER_ITEMS oi ON 
                                    od.ORDER_ID = oi.ORDER_ID
                                LEFT JOIN FOOD_ITEM fi ON
	                                oi.FOOD_ITEM_ID = fi.ITEM_ID
                                WHERE od.DATE_RECEIVED = date(?);
                                """
            c.execute(sql_query_string, (date,))
            rows = c.fetchall()
            for row in rows:
                if food_item_id_to_qty.get(row["FOOD_ITEM_ID"]) is not None:
                    food_item_id_to_qty.get(row["FOOD_ITEM_ID"]).quantity += int(row["QUANTITY"])
                else:
                    food_item_id_to_qty[row["FOOD_ITEM_ID"]] = SummaryFoodItem(row["FOOD_ITEM_ID"], int(row["QUANTITY"]), row["DESCRIPTION"], row["DESCRIPTION_CHINESE"])
        return food_item_id_to_qty