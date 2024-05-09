from escpos.constants import TXT_SIZE, ESC
from escpos.printer import Usb, Dummy
import os
import six
import datetime

from FoodOrderUseCases import DeliveryMethod, FoodOrder
from interfaces.Customer import Customer
from interfaces.FoodItem import FoodItem

TEXT_SIZE_DOUBLE = TXT_SIZE + b'\x11'
SMALL_SIZE_COMMAND = TXT_SIZE + six.int2byte(0)
CHINESE_MODE= ESC + b'\x52' + six.int2byte(15)
JUSTIFICATION_PREFIX = ESC + b'\x61'
CENTER = JUSTIFICATION_PREFIX + six.int2byte(1)
LEFT = JUSTIFICATION_PREFIX + six.int2byte(0)
RIGHT = JUSTIFICATION_PREFIX + six.int2byte(2)


# How do I add libusb to PATH?
usbLibPath1 = "C:/Users/Hansw/Projects/ChowsPOS/myEnv/Lib/site-packages/libusb/_platform/_windows/x64"
if not usbLibPath1 in os.environ["PATH"]:
    # print("add new path")
    os.environ["PATH"]+=usbLibPath1

def get_printer():
    try:
        return Usb(0x0483, 0x5743)
    except:
        print("Not Printer found, going to dummy mode")
        return Dummy()


def print_line_divider_center_small(printer):
    printer._raw(CENTER)
    printer._raw(SMALL_SIZE_COMMAND)
    printer.textln('-'*24)


# print(os.environ["PATH"])
def print_collection_chinese_order(printer, food_order: FoodOrder):
    printer._raw(SMALL_SIZE_COMMAND)
    # Customer Information
    printer._raw(LEFT)
    printer.textln(f'Name: {food_order.customer.name}')
    printer.textln(f'Phone: {food_order.customer.telephone}')
    now = datetime.datetime.now().strftime('%H:%M:%S')
    printer.textln(f'Order Time: {now}')
    print_line_divider_center_small(printer)
    printer._raw(TEXT_SIZE_DOUBLE)
    printer.textln('COLLECTION')
    print_line_divider_center_small(printer)
    printer._raw(LEFT)
    # Set Chinese codepage
    printer._raw(ESC + b'\x52' + six.int2byte(15))
    # 
    for food in food_order.ordered_food_items:
        printer._raw(TEXT_SIZE_DOUBLE)
        qty = str(food.quantity).ljust(3,  ' ')
        chinese = food.description_chinese.ljust(13,  ' ')
        # Can add modifications here
        chinese = chinese if len(food.description_chinese) % 2 == 0 else chinese + ' '
        number = str(food.item_number).rjust(4,  ' ')
        printer._raw((qty+chinese+number).encode('CP950'))
        printer.ln()
        printer._raw(SMALL_SIZE_COMMAND)
        printer.textln((6*' '+food.description))
        printer.textln('-'*(24*2))

    printer._raw(CENTER)
    printer.textln('-'*24*2)
    # Print Order Number and Total price
    printer._raw(TEXT_SIZE_DOUBLE)

    price = food_order.get_total_price()
    printer._raw(LEFT)
    printer._raw(str(food_order.order_id).ljust(10,  ' '))
    printer._raw("TOTAL: ")
    printer._raw(str(price).rjust(7,  ' '))
    printer.cut()

def print_english_order(printer: Usb, food_order: FoodOrder):
    printer._raw(SMALL_SIZE_COMMAND)
    # Customer Information
    printer._raw(LEFT)
    printer.textln(f'Name: {food_order.customer.name}')
    printer.textln(f'Phone: {food_order.customer.telephone}')
    now = datetime.datetime.now().strftime('%H:%M:%S')
    printer.textln(f'Order Time: {now}')
    print_line_divider_center_small(printer)
    printer._raw(TEXT_SIZE_DOUBLE)
    printer.textln('COLLECTION')
    print_line_divider_center_small(printer)
    printer._raw(LEFT)
    for food in food_order.ordered_food_items:
        number = str(food.item_number).ljust(6,  ' ')
        qty = str(food.quantity).ljust(2,  ' ')
        dish = food.description.ljust(13*2,  ' ')
        price = str(food.unit_price*food.quantity).rjust(6,  ' ')
        printer._raw((' '*4+number+qty+dish+price).encode('CP950'))
        printer.ln()
    
    printer._raw(CENTER)
    printer.textln('-'*24*2)
    # Print Order Number and Total price
    printer._raw(TEXT_SIZE_DOUBLE)

    price = food_order.get_total_price()
    printer._raw(LEFT)
    printer._raw(str(food_order.order_id).ljust(10,  ' '))
    printer._raw("TOTAL: ")
    printer._raw(str(price).rjust(7,  ' '))
    printer.cut()