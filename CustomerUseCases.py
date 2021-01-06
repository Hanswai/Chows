from interfaces.Customer import Customer
from db_variables import CHOWS_MAIN_DB
import sqlite3 as db

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class CustomerUseCases:

    def get_contact(self, telephone):
        connection = db.connect(CHOWS_MAIN_DB)
        connection.row_factory = dict_factory
        with connection:
            c = connection.cursor()
            c.execute("SELECT * FROM CUSTOMER WHERE TELEPHONE = ?", (telephone,))
            result = c.fetchone()
            if result:
                customer = Customer(result['NAME'], result['TELEPHONE'], result['ADDRESSLINE1'], result['ADDRESSLINE2'], result['POSTCODE'])
                customer.setId(result['CUSTOMER_ID'])
                return customer
        return None

    def add_new_contact(self, contact):
        """Add new Customer - overwrites if it already exists."""
        connection = db.connect(CHOWS_MAIN_DB)
        with connection:
            c = connection.cursor()
            db_contact = self.get_contact(contact.telephone)
            insert_db = (contact.telephone, contact.name, contact.address1, contact.address2, contact.postcode, contact.comments)
            if db_contact is not None:
                c.execute("""   UPDATE CUSTOMER 
                                SET
                                    TELEPHONE = ?, 
                                    NAME = ?, 
                                    ADDRESSLINE1 = ?, 
                                    ADDRESSLINE2 = ?, 
                                    POSTCODE = ?, 
                                    COMMENTS = ?
                                WHERE CUSTOMER_ID = ?""", (  contact.telephone, 
                                                            contact.name, 
                                                            contact.address1, 
                                                            contact.address2, 
                                                            contact.postcode, 
                                                            contact.comments, 
                                                            db_contact.id))
                contact.setId(db_contact.id)
            else:
                c.execute("INSERT INTO CUSTOMER(TELEPHONE, NAME, ADDRESSLINE1, ADDRESSLINE2, POSTCODE, COMMENTS) VALUES (?,?,?,?,?,?)", insert_db)
                contact.setId(c.lastrowid)
            connection.commit()
            return contact
        return None