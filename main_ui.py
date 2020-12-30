from PyQt5 import QtCore, QtGui, QtWidgets

from interfaces.ContactInformation import ContactInformation
from ContactInformationUseCases import ContactInformationUseCases
from FoodOrderUseCases import FoodOrder 

class Ui_MainWindow(object):
    def __init__(self):
        # The main food order which the main window will keep track of.
        self.food_order = FoodOrder()

    def display_contact(self, contact):
        self.nameLineEdit.setText(contact.name)
        self.address1LineEdit.setText(contact.address1)
        self.address2LineEdit.setText(contact.address2)
        self.postcodeLineEdit.setText(contact.postcode)

    def get_contact_information_display(self):
        display_string = ""
        display_string += "Hello " + self.nameLineEdit.text() + ", "
        display_string += self.address1LineEdit.text() + " "
        display_string += self.address2Label.text() + ", "
        display_string += self.postcodeLineEdit.text() + "."
        display_string += "You can contact with " + self.telLineEdit.text()
        return display_string

    def clear_contact_display(self):
        self.nameLineEdit.clear()
        self.address1LineEdit.clear()
        self.address2LineEdit.clear()
        self.postcodeLineEdit.clear()

    def refresh_display(self):
        self.tableWidget.setRowCount(0)
        for i in self.food_order.get_all_food_items():
            self.add_food_row(i)
        self.totalPriceDisplayLabel.setText("{:,.2f}".format(self.food_order.get_total_price()))

    def handle_enter(self):
        contact = ContactInformation(self.nameLineEdit.text(),
                                     self.telLineEdit.text(),
                                     self.address1LineEdit.text(),
                                     self.address2LineEdit.text(),
                                     self.postcodeLineEdit.text())

        ContactInformationUseCases().add_new_contact(contact)

    def handle_search_enter(self):
        if self.telLineEdit.text() != "":
            contact = ContactInformationUseCases().get_contact(self.telLineEdit.text())
            if contact is not None:
                self.display_contact(contact)
            else:
                self.clear_contact_display()
    
    def handle_order_enter(self):
        if self.enterDishLineEdit.text() != "":
            food_item = self.food_order.get_food_item(self.enterDishLineEdit.text())
            self.food_order.add_to_food_order(food_item)
            self.enterDishLineEdit.clear()
        self.refresh_display()

    def add_food_row(self, food_item):
        if food_item is not None:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            food_info_to_display = (food_item.item_number,
                                    food_item.description,
                                    food_item.description_chinese,
                                    food_item.note,
                                    food_item.quantity,
                                    food_item.display_price_string())
            print(food_info_to_display)
            for i in range(self.tableWidget.columnCount()):
                item = QtWidgets.QTableWidgetItem(str(food_info_to_display[i]) if food_info_to_display[i] else "")
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, i, item)
            self.tableWidget.scrollToBottom()

    def handle_print_button(self):
        self.food_order.save_order_to_db()

    def setup_connects(self):
        self.telLineEdit.returnPressed.connect(self.handle_search_enter)
        self.postcodeLineEdit.returnPressed.connect(self.handle_enter)
        self.address1LineEdit.returnPressed.connect(self.handle_enter)
        self.address2LineEdit.returnPressed.connect(self.handle_enter)
        self.nameLineEdit.returnPressed.connect(self.handle_enter)

    def setup_contact_form(self):
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(660, 30, 331, 181))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.teleLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.teleLabel.setObjectName("teleLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.teleLabel)
        self.telLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.telLineEdit.setObjectName("telLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.telLineEdit)
        self.postcodeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.postcodeLabel.setObjectName("postcodeLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.postcodeLabel)
        self.postcodeLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.postcodeLineEdit.setObjectName("postcodeLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.postcodeLineEdit)
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.address1Label = QtWidgets.QLabel(self.formLayoutWidget)
        self.address1Label.setObjectName("address1Label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.address1Label)
        self.address1LineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.address1LineEdit.setObjectName("address1LineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.address1LineEdit)
        self.address2Label = QtWidgets.QLabel(self.formLayoutWidget)
        self.address2Label.setText("")
        self.address2Label.setObjectName("address2Label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.address2Label)
        self.address2LineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.address2LineEdit.setObjectName("address2LineEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.address2LineEdit)
        self.nameLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.nameLabel.setObjectName("nameLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.nameLabel)
        self.nameLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.nameLineEdit)

    def setup_order_table(self):
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 30, 631, 341))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        for i in range(6):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)
        #Total Price Section
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(430, 390, 201, 31))
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.totalPriceLabel = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.totalPriceLabel.setObjectName(u"totalPriceLabel")
        font1 = QtGui.QFont()
        font1.setPointSize(14)
        self.totalPriceLabel.setFont(font1)

        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.totalPriceLabel)

        self.totalPriceDisplayLabel = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.totalPriceDisplayLabel.setObjectName(u"totalPriceDisplayLabel")
        self.totalPriceDisplayLabel.setFont(font1)

        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.totalPriceDisplayLabel)    
    
    def setup_order_field(self):
        self.enterDishLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.enterDishLineEdit.setObjectName(u"enterDishLineEdit")
        self.enterDishLineEdit.setGeometry(QtCore.QRect(280, 380, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.enterDishLineEdit.setFont(font)
        self.enterDishLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.enterDishLineEdit.setText("")

        self.enterDishLineEdit.returnPressed.connect(self.handle_order_enter)

    def setup_print_button(self):
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QtCore.QRect(760, 290, 111, 71))
        self.pushButton.setText(QtCore.QCoreApplication.translate("MainWindow", u"PRINT", None))

        self.pushButton.clicked.connect(self.handle_print_button)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.setup_contact_form()
        self.setup_order_table()
        self.setup_order_field()

        self.setup_print_button()

        #self.noteLabel = QtWidgets.QLabel(self.formLayoutWidget)
        #self.noteLabel.setText("")
        #self.noteLabel.setObjectName("noteLabel")
        #self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.noteLabel)
        #self.noteLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        #self.noteLineEdit.setObjectName("noteLineEdit")
        #self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.noteLineEdit)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.setup_connects()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.teleLabel.setText(_translate("MainWindow", "Phone No: "))
        self.postcodeLabel.setText(_translate("MainWindow", "Postcode: "))
        self.address1Label.setText(_translate("MainWindow", "Address:"))
        self.nameLabel.setText(_translate("MainWindow", "Name: "))
        #self.noteLabel.setText(_translate("MainWindow", "Customer Note: "))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "No."))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Dish"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "食品"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Note"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Quantity"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Price"))

        self.totalPriceLabel.setText(_translate("MainWindow", u"Total Price: £", None))
        self.totalPriceDisplayLabel.setText("")

