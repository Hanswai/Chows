# from ChowsPrinter import print_collection_chinese_order, print_english_order
# from escpos.printer import Usb


# from FoodOrderUseCases import DeliveryMethod, FoodOrder
# from interfaces.Customer import Customer
# from interfaces.FoodItem import Dish

COMMON_CHINESE_CHARACTER = (0x4E00,0x9FFF)

if __name__ == "__main__":
    # food_items = [ Dish(173, 4.00, 1, "Egg Fried Rice", "蛋炒飯"),
    #               Dish(164, 7.00, 1, "Singapore Rice Noodles", "星洲米粉")
    #               ]
    # name = "Hans"
    # phone = "07473149671"
    # customer = Customer(name, phone)

    # food_order = FoodOrder()
    # food_order.ordered_dishes = food_items
    # food_order.delivery_method = DeliveryMethod.COLLECTION
    # food_order.customer = customer
    # food_order.order_id = 7
    # # How do I prepare this Usb?
    # printer = Usb(0x0483, 0x5743)
    
    # print_english_order(printer, food_order)
    # # print_collection_chinese_order(printer, food_order)

    # printer.cut()

    # character = COMMON_CHINESE_CHARACTER[0]
    # print(chr(character))

    print(hex(ord('麵')))
    print(chr(0x9eb5))


    characters = [chr(COMMON_CHINESE_CHARACTER[0]+i) for i in range(1000)]

    print(characters)
