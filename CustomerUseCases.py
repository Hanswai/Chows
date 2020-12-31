from interfaces.Customer import Customer

import sqlite3 as db

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class CustomerUseCases:

    def get_contact(self, telephone):
        connection = db.connect('chows_db.db')
        connection.row_factory = dict_factory
        with connection:
            c = connection.cursor()
            c.execute("SELECT * FROM CUSTOMER WHERE TELEPHONE = ?", (telephone,))
            result = c.fetchone()
            connection.close()
            if result:
                customer = Customer(result['NAME'], result['TELEPHONE'], result['ADDRESSLINE1'], result['ADDRESSLINE2'], result['POSTCODE'])
                customer.setId(result['CUSTOMER_ID'])
                return customer
        return None

    def add_new_contact(self, contact):
        # TODO: Check for exisitng matching Customer before Adding new contact.
        connection = db.connect('chows_db.db')
        c = connection.cursor()
        insert_db = (contact.telephone, contact.name, contact.address1, contact.address2, contact.postcode, contact.comments)
        c.execute("INSERT INTO CUSTOMER(TELEPHONE, NAME, ADDRESSLINE1, ADDRESSLINE2, POSTCODE, COMMENTS) VALUES (?,?,?,?,?,?)", insert_db)
        print(c.lastrowid)
        contact.setId(c.lastrowid)
        connection.commit()
        connection.close()
