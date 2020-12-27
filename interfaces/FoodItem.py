class FoodItem:
    def __init__(self, item_number, price, quantity, description="", description_chinese=""):
        self.item_number = item_number
        self.price = price
        self.description = description
        self.description_chinese = description_chinese
        self.quantity = quantity
        self.note = ""
    
    def isComplete(self):
        return self.description != "" and self.price != "" and self.description_chinese != ""

    def add_note(self, note):
        self.note = note
    
    def display_price_string(self):
        return "{:,.2f}".format(self.price)