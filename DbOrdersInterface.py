""" A Bunch of ultity functions to interface with DB"""

from interfaces.SummaryFoodItem import SummaryFoodItem
import sqlite3 as db
from enum import Enum
from datetime import datetime
from db_variables import CHOWS_MAIN_DB



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DbOrders:
    @staticmethod
    def retrieve_total_price_by_date(date):
        connection = db.connect(CHOWS_MAIN_DB)
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
    def retrieve_dishes_and_qty_by_date(date):
        connection = db.connect(CHOWS_MAIN_DB)
        connection.row_factory = dict_factory
        dish_id_to_qty = {}
        with connection:
            c = connection.cursor()
            sql_query_string = """            
                                SELECT 
                                    oi.FOOD_ITEM_ID, 
                                    oi.QUANTITY, 
                                    d.DESCRIPTION,
                                    d.DESCRIPTION_CHINESE
                                FROM ORDER_DETAILS od 
                                INNER JOIN ORDER_ITEMS oi ON 
                                    od.ORDER_ID = oi.ORDER_ID
                                LEFT JOIN DISH d ON
	                                oi.FOOD_ITEM_ID = d.ID
                                WHERE od.DATE_RECEIVED = date(?);
                                """
            c.execute(sql_query_string, (date,))
            rows = c.fetchall()
            for row in rows:
                if dish_id_to_qty.get(row["FOOD_ITEM_ID"]) is not None:
                    dish_id_to_qty.get(row["FOOD_ITEM_ID"]).quantity += int(row["QUANTITY"])
                else:
                    dish_id_to_qty[row["FOOD_ITEM_ID"]] = SummaryFoodItem(row["FOOD_ITEM_ID"], int(row["QUANTITY"]), row["DESCRIPTION"], row["DESCRIPTION_CHINESE"])
        return dish_id_to_qty
    
    @staticmethod
    def retrieve_total_price_by_date_range(start_date, end_date):
        connection = db.connect(CHOWS_MAIN_DB)
        connection.row_factory = dict_factory
        sum = 0
        with connection:
            c = connection.cursor()
            c.execute("SELECT TOTAL_PRICE FROM ORDER_DETAILS WHERE DATE_RECEIVED between date(?) and date(?)", (start_date,end_date,))
            rows = c.fetchall()
            for row in rows:                
                sum += float(row['TOTAL_PRICE'])
            return sum
        return 0
    @staticmethod
    def retrieve_food_items_and_qty_by_date_range(start_date, end_date):
        connection = db.connect(CHOWS_MAIN_DB)
        connection.row_factory = dict_factory
        food_item_id_to_qty = {}
        with connection:
            c = connection.cursor()
            sql_query_string = """            
                                SELECT 
                                    oi.FOOD_ITEM_ID, 
                                    oi.QUANTITY, 
                                    d.DESCRIPTION,
                                    d.DESCRIPTION_CHINESE
                                FROM ORDER_DETAILS od 
                                INNER JOIN ORDER_ITEMS oi ON 
                                    od.ORDER_ID = oi.ORDER_ID
                                LEFT JOIN DISH d ON
	                                oi.FOOD_ITEM_ID = d.ID
                                WHERE od.DATE_RECEIVED between date(?) and date(?);
                                """
            c.execute(sql_query_string, (start_date, end_date,))
            rows = c.fetchall()
            for row in rows:
                if food_item_id_to_qty.get(row["FOOD_ITEM_ID"]) is not None:
                    food_item_id_to_qty.get(row["FOOD_ITEM_ID"]).quantity += int(row["QUANTITY"])
                else:
                    food_item_id_to_qty[row["FOOD_ITEM_ID"]] = SummaryFoodItem(row["FOOD_ITEM_ID"], int(row["QUANTITY"]), row["DESCRIPTION"], row["DESCRIPTION_CHINESE"])
        return food_item_id_to_qty

    @staticmethod
    def delete_orders_by_date_range(start_date, end_date):
        connection = db.connect(CHOWS_MAIN_DB)
        with connection:
            c = connection.cursor()
            select_id_query_string = "SELECT ORDER_ID FROM ORDER_DETAILS WHERE DATE_RECEIVED between date(?) AND date(?)"
            c.execute(select_id_query_string, (start_date, end_date,))
            ids_to_delete = c.fetchall()
            if len(ids_to_delete) > 0:
                delete_order_items_query_string = """
                                    DELETE FROM ORDER_ITEMS WHERE ORDER_ID = ?;
                                    """
                delete_orders_query_string = """
                                    DELETE FROM ORDER_DETAILS WHERE ORDER_ID = ?;
                                    """                                
                c.executemany(delete_order_items_query_string, ids_to_delete)
                c.executemany(delete_orders_query_string, ids_to_delete)
                print("Deleted " + str(len(ids_to_delete)) + " orders." )
                connection.commit()
            else:
                print("Nothing to delete")
        
