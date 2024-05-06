class Customer:
    def __init__(self, name="", telephone="", address1="", address2="", postcode=""):
        self.name = name
        self.telephone = telephone
        self.address1 = address1
        self.address2 = address2
        self.postcode = postcode
        self.comments = ""
        self.id = None

    def __str__(self):
        return "('{0}', {1}, {2}, {3}, {4})".format(self.name, self.telephone, self.address1, self.address2,
                                                    self.postcode)

    def setId(self, id):
        self.id = id
    
    def set_comment(self, comment):
        self.comment = comment
