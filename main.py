import sqlite3

from interfaces.ContactInformation import ContactInformation


connection = sqlite3.connect('contactInfo.db')

c = connection.cursor()

# Create table
c.execute("DROP TABLE contactInfo")
c.execute('''CREATE TABLE contactInfo
             (telephone text, name text, address1 text, address2 text, postcode text)''')

me = ContactInformation('Wai', '02085402095', '77 Hillcross Ave', 'Morden', 'SM44AY')

insertDb = (me.telephone, me.name, me.address1, me.address2, me.postcode,)

c.execute("INSERT INTO contactInfo VALUES (?,?,?, ?, ?)", insertDb)

c.execute("SELECT * FROM contactInfo WHERE telephone = ?", (me.telephone,))
print(c.fetchone())

connection.commit()

connection.close()