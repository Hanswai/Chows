from interfaces.ContactInformation import ContactInformation

import sqlite3 as db

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class ContactInformationUseCases:

    def get_contact(self, telephone):
        connection = db.connect('contactInfo.db')
        connection.row_factory = dict_factory
        with connection:
            c = connection.cursor()
            c.execute("SELECT * FROM contactInfo WHERE telephone = ?", (telephone,))
            result = c.fetchone()
            if result:
                return ContactInformation(result['name'], result['telephone'], result['address1'], result['address2'], result['postcode'])
        return None

    def add_new_contact(self, contact):
        connection = db.connect('contactInfo.db')
        c = connection.cursor()
        insert_db = (contact.telephone, contact.name, contact.address1, contact.address2, contact.postcode,)
        c.execute("INSERT INTO contactInfo VALUES (?,?,?, ?, ?)", insert_db)
        connection.commit()
        connection.close()
