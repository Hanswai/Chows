class FoodItem:
    def __init__(self, item_number, price, quantity, description="", description_chinese=""):
        self.item_number = item_number
        self.unit_price = price
        self.description = description
        self.description_chinese = description_chinese
        self.quantity = quantity
        self.note = ""
    
    def isComplete(self):
        return self.description != "" and self.unit_price != "" and self.description_chinese != ""

    def add_note(self, note):
        self.note = note
    
    def get_total_price(self):
        return self.unit_price*self.quantity

    def display_price_string(self):
        return "{:,.2f}".format(self.unit_price*self.quantity)