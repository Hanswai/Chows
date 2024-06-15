class Dish:
    def __init__(self, id, price, quantity, description="", description_chinese=""):
        self.id = id
        self.unit_price = price
        self.description = description
        self.description_chinese = description_chinese
        self.quantity = quantity
        self.note = ""
        self.categories = []
    
    def isComplete(self):
        return self.description != "" and self.unit_price != "" and self.description_chinese != ""

    def add_note(self, note):
        self.note = note
    
    def get_total_price(self):
        return self.unit_price*self.quantity

    def display_price_string(self):
        return "{:,.2f}".format(self.unit_price*self.quantity)

    def serialise_categories(self):
        return "|".join(self.categories)
    
    def deserialise_categories(self, raw_string: str):
        return raw_string.split("|") if raw_string is not None else []
