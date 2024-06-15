from PyQt5 import QtCore, QtGui, QtWidgets

from ChowsPrinter import get_printer, print_english_order
from UI.dialog import NoActionDialog
from UI.dish_window import DishWindow
from interfaces.Customer import Customer
from CustomerUseCases import CustomerUseCases
from FoodOrderUseCases import FoodNotFoundException, FoodOrder

from DbDishInterface import DbDish

from UI.summary_ui import SummaryWindow
from datetime import datetime

NOTE_COLUMN_NUMBER = 3

class ChowsMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # The main food order which the main window will keep track of.
        super(ChowsMainWindow, self).__init__(parent)
        self.food_order = FoodOrder()
        self.setupUi(self)
        self.retranslateUi(self)

    def display_contact(self, contact):
        self.telLineEdit.setText(contact.telephone)
        self.nameLineEdit.setText(contact.name)
        self.address1LineEdit.setText(contact.address1)
        self.address2LineEdit.setText(contact.address2)
        self.postcodeLineEdit.setText(contact.postcode)

    def clear_contact_display(self):
        self.nameLineEdit.clear()
        self.address1LineEdit.clear()
        self.address2LineEdit.clear()
        self.postcodeLineEdit.clear()
        self.noteLineEdit.clear()

    def refresh_display(self):
        self.tableWidget.setRowCount(0)
        for i in self.food_order.get_all_dishes():
            self.add_food_row(i)
        self.totalPriceDisplayLabel.setText(
            "{:,.2f}".format(self.food_order.get_total_price()))

    def save(self, food_order: FoodOrder):
        food_order.save_order_to_db()
        CustomerUseCases().add_new_contact(food_order.customer)


    def handle_enter(self):
        pass

    def handle_search_enter(self):
        if self.telLineEdit.text() != "":
            contact = CustomerUseCases().get_contact(self.telLineEdit.text())
            if contact is not None:
                self.display_contact(contact)
            else:
                self.clear_contact_display()

    def handle_order_enter(self):
        if self.enterDishLineEdit.text() != "":
            try:
                food_item = self.food_order.get_food_item(
                    self.enterDishLineEdit.text())
                self.food_order.add_to_food_order(food_item)
                self.enterDishLineEdit.clear()
            except FoodNotFoundException as e:
                self.displayFoodNotFoundDialog(e.food_id)
        self.refresh_display()

    def displayFoodNotFoundDialog(self, food_id):
        NoActionDialog(food_id).exec()


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
                item = QtWidgets.QTableWidgetItem(
                    str(food_info_to_display[i]) if food_info_to_display[i] else "")
                
                self.tableWidget.setItem(
                    self.tableWidget.rowCount()-1, i, item)
            self.tableWidget.scrollToBottom()

    def handle_collection_button(self):
        if self.telLineEdit.text() != "":
            self.food_order.set_delivery_method("COLLECTION")
        else:
            self.food_order.set_delivery_method("PRESENT")

        customer = self.extract_customer()
        printer = get_printer()
        self.food_order.set_customer(customer)
        self.save(self.food_order)
        print_english_order(printer, self.food_order)
        self.food_order.reset()
        self.telLineEdit.clear()
        self.clear_contact_display()
        self.refresh_display()

    def handle_delivery_button(self):
        self.food_order.set_delivery_method("DELIVERY")
        customer = self.extract_customer()
        printer = get_printer()
        self.food_order.set_customer(customer)
        self.save(self.food_order)

        self.food_order.reset()
        self.telLineEdit.clear()
        self.clear_contact_display()
        self.refresh_display()
    
    def extract_customer(self):
        if self.telLineEdit.text() != "":
            contact = Customer(self.nameLineEdit.text(),
                            self.telLineEdit.text(),
                            self.address1LineEdit.text(),
                            self.address2LineEdit.text(),
                            self.postcodeLineEdit.text())
            contact.set_comment(self.noteLineEdit.text())
            self.food_order.set_customer(contact)
            return contact
        return Customer()

    def handle_table_cell_edited(self, item):
        if item.column() == NOTE_COLUMN_NUMBER and item.text() != "":
            food_id = self.tableWidget.item(item.row(), 0).text()
            food_item = self.food_order.get_food_item(food_id)
            food_item.add_note(item.text())

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
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.teleLabel)
        self.telLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.telLineEdit.setObjectName("telLineEdit")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.telLineEdit)
        self.postcodeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.postcodeLabel.setObjectName("postcodeLabel")
        self.nameLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.nameLabel.setObjectName("nameLabel")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.nameLabel)
        self.nameLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.nameLineEdit)        
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.postcodeLabel)
        self.postcodeLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.postcodeLineEdit.setObjectName("postcodeLineEdit")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.postcodeLineEdit)
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.address1Label = QtWidgets.QLabel(self.formLayoutWidget)
        self.address1Label.setObjectName("address1Label")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.LabelRole, self.address1Label)
        self.address1LineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.address1LineEdit.setObjectName("address1LineEdit")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.FieldRole, self.address1LineEdit)
        self.address2Label = QtWidgets.QLabel(self.formLayoutWidget)
        self.address2Label.setText("")
        self.address2Label.setObjectName("address2Label")
        self.formLayout.setWidget(
            5, QtWidgets.QFormLayout.LabelRole, self.address2Label)
        self.address2LineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.address2LineEdit.setObjectName("address2LineEdit")
        self.formLayout.setWidget(
            5, QtWidgets.QFormLayout.FieldRole, self.address2LineEdit)

        self.noteLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.noteLabel.setText("")
        self.noteLabel.setObjectName("noteLabel")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.noteLabel)
        self.noteLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.noteLineEdit.setObjectName("noteLineEdit")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.noteLineEdit)            

    def setup_order_table(self):
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 30, 631, 341))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)

        self.tableWidget.setRowCount(0)
        for i in range(6):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)
        # Total Price Section
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(430, 390, 201, 31))
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFormAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.totalPriceLabel = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.totalPriceLabel.setObjectName(u"totalPriceLabel")
        font1 = QtGui.QFont()
        font1.setPointSize(14)
        self.totalPriceLabel.setFont(font1)
        self.formLayout_2.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.totalPriceLabel)

        self.totalPriceDisplayLabel = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.totalPriceDisplayLabel.setObjectName(u"totalPriceDisplayLabel")
        self.totalPriceDisplayLabel.setFont(font1)
        self.formLayout_2.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.totalPriceDisplayLabel)
        
        self.tableWidget.itemChanged.connect(self.handle_table_cell_edited)

    def setup_order_field(self):
        self.enterDishLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.enterDishLineEdit.setObjectName(u"enterDishLineEdit")
        self.enterDishLineEdit.setGeometry(QtCore.QRect(280, 380, 111, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.enterDishLineEdit.setFont(font)
        self.enterDishLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.enterDishLineEdit.setText("")

        self.enterDishLineEdit.returnPressed.connect(self.handle_order_enter)
        self.enterDishLineEdit.textChanged.connect(self.update_suggestion_box_by_id)

    def setup_suggestion_table(self):
        self.suggest_table_widget = QtWidgets.QTableWidget(self.centralwidget)
        self.suggest_table_widget.setObjectName("suggest_table_widget")
        self.suggest_table_widget.setGeometry(QtCore.QRect(20, 450, 631, 211))

        self.suggest_table_widget.setColumnCount(4)
        self.suggest_table_widget.setRowCount(0)

        header = self.suggest_table_widget.horizontalHeader()
        item0 = QtWidgets.QTableWidgetItem()
        item0.setText("No.")
        self.suggest_table_widget.setHorizontalHeaderItem(0, item0)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        item1 = QtWidgets.QTableWidgetItem()
        item1.setText("Dish")
        self.suggest_table_widget.setHorizontalHeaderItem(1, item1) 
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        item2 = QtWidgets.QTableWidgetItem()
        item2.setText("食品")
        self.suggest_table_widget.setHorizontalHeaderItem(2, item2)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        item3 = QtWidgets.QTableWidgetItem()
        item3.setText("Price")
        self.suggest_table_widget.setHorizontalHeaderItem(3, item3)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)        
        
    def add_suggestion_row(self, dish):
        if dish is not None:
            self.suggest_table_widget.insertRow(self.suggest_table_widget.rowCount())
            food_info_to_display = (dish.id,
                                    dish.description,
                                    dish.description_chinese,
                                    dish.display_price_string())
            for i in range(self.suggest_table_widget.columnCount()):
                item = QtWidgets.QTableWidgetItem(
                    str(food_info_to_display[i]) if food_info_to_display[i] else "")
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)                    
                self.suggest_table_widget.setItem(
                    self.suggest_table_widget.rowCount()-1, i, item)
            self.suggest_table_widget.scrollToBottom()

    def update_suggestion_box_by_id(self, id):
        dishes = DbDish.retrieve_dishes_by_id_like(id)
        self.suggest_table_widget.setRowCount(0)
        for dish in dishes:
            self.add_suggestion_row(dish)

    def update_suggestion_box(self, text):
        dishes = DbDish.retrieve_dishes_by_description(text)
        self.suggest_table_widget.setRowCount(0)
        for dish in dishes:
            self.add_suggestion_row(dish)
        
    def summary_dialog_window(self):
        self.dialog = SummaryWindow()
        self.dialog.show()

    def edit_dish_window(self, MainWindow):
        DishWindow().exec_()

    def setup_collection_button(self):
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QtCore.QRect(690, 580, 121, 81))
        self.pushButton.setText("COLLECTION")
        self.pushButton.clicked.connect(self.handle_collection_button)

    def setup_delivery_button(self):
        self.delivery_button = QtWidgets.QPushButton(self.centralwidget)
        self.delivery_button.setObjectName(u"delivery_button")
        self.delivery_button.setGeometry(QtCore.QRect(850, 580, 121, 81))
        self.delivery_button.setText("DELIVERY")
        self.delivery_button.clicked.connect(self.handle_delivery_button)        

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.setup_contact_form()
        self.setup_order_table()
        self.setup_order_field()

        self.setup_collection_button()
        self.setup_delivery_button()

        self.setup_suggestion_table()
        # Search Bar for suggestion Box
        self.setup_search_bar()

        self.actionSummary = QtWidgets.QAction(MainWindow)
        self.actionSummary.setObjectName(u"actionSummary")
        self.actionEditMenu = QtWidgets.QAction(MainWindow)
        self.actionEditMenu.setObjectName(u"actionEditMenu")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")  
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuView.menuAction())
        self.menuView.addAction(self.actionSummary)
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menuEdit.addAction(self.actionEditMenu)
        self.menuEdit.setTitle("Edit")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.setup_connects()
        self.actionSummary.triggered.connect(self.summary_dialog_window)
        self.menuEdit.triggered.connect(self.edit_dish_window)

    def setup_search_bar(self):
        # Search Bar for suggestion Box
        font1 = QtGui.QFont()
        font1.setPointSize(14)
        self.searchLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.searchLineEdit.setObjectName(u"searchLineEdit")
        self.searchLineEdit.setGeometry(QtCore.QRect(40, 389, 141, 41))
        self.searchLineEdit.setFont(font1)

        self.searchLineEdit.textChanged.connect(self.update_suggestion_box)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle("Wai Wai POS")

        self.actionSummary.setText("Summary")
        self.actionEditMenu.setText("Edit Menu")

        self.teleLabel.setText("Phone No: ")
        self.nameLabel.setText("Name: ")
        self.postcodeLabel.setText("Postcode: ")
        self.address1Label.setText("Address:")
        self.noteLabel.setText("Customer Note: ")
        header = self.tableWidget.horizontalHeader()
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "No."))
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Dish"))
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "食品"))
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Note"))
        header.setSectionResizeMode(NOTE_COLUMN_NUMBER, QtWidgets.QHeaderView.Stretch)
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Quantity"))
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Price"))
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

        self.totalPriceLabel.setText(_translate("MainWindow", u"Total Price: £", None))
        self.totalPriceDisplayLabel.setText("")
        self.menuView.setTitle(_translate("MainWindow", u"View", None))
