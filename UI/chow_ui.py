from PyQt5.QtWidgets import *
from PyQt5.QtGui  import QColorConstants, QFont
from PyQt5.QtCore import Qt, QSize
from CustomerUseCases import CustomerUseCases
from FoodOrderUseCases import FoodNotFoundException, FoodOrder
from interfaces.Customer import Customer
from UI.dish_window import CATEGORIES

OPTIONS = ['Exit Application', 'Menu', 'Address','Select Printer','View Menu','Administrator','Call ID','Save','View Order','Paper Setting','Company VAT No.','View Address','Protection','Edit Order','Previous','Order On Hold','Summary','Receipt']



class ChowsWindow(QMainWindow):
    def __init__(self, parent=None):
        # The main food order which the main window will keep track of.
        super(ChowsWindow, self).__init__(parent)
        self.food_order = FoodOrder()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)   

        self.main_layout = QHBoxLayout(central_widget)
        
        food_layout = QVBoxLayout()
        self.food_order_table = self.build_food_order_table()
        food_layout.addWidget(self.food_order_table)

        middle_food_layout = QHBoxLayout()
        self.dish_id_input = self.setup_dish_id_input()
        food_layout.addLayout(middle_food_layout)
        middle_food_layout.addLayout(self.setup_order_number_counter())
        middle_food_layout.addWidget(self.dish_id_input)
        middle_food_layout.addLayout(self.setup_order_total_price())
        
        self.dish_suggestion_table = self.build_dish_suggestion_table()
        food_layout.addWidget(self.dish_suggestion_table)

        self.other_stuff_layout = QVBoxLayout()
        self.other_stuff_layout.addLayout(self.build_contact_form())
        self.other_stuff_layout.addLayout(self.build_grid_selectors())
        self.grid_stacked_layout = self.build_stacked_layout()
        self.other_stuff_layout.addLayout(self.grid_stacked_layout)


        self.main_layout.addLayout(food_layout)
        self.main_layout.addLayout(self.other_stuff_layout)


        #self.showMaximized()


    ###
    #   Food Order related UI
    ###
    def build_food_order_table(self):
        food_order_table = QTableWidget()
        column_names = ['No.', 'Dish', '食品', 'Note', 'Quantity', 'Price']

        food_order_table.setColumnCount(len(column_names))
        food_order_table.setRowCount(0)

        food_order_table.setHorizontalHeaderLabels(column_names)
        food_order_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return food_order_table
    
    def setup_dish_id_input(self):
        main_dish_id_input = QLineEdit()
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        main_dish_id_input.setFont(font)
        main_dish_id_input.setAlignment(Qt.AlignCenter)

        # self.main_dish_id_input.returnPressed.connect(self.handle_order_enter)
        # self.main_dish_id_input.textChanged.connect(self.update_suggestion_box_by_id)
        return main_dish_id_input

    def setup_order_number_counter(self):
        counter_layout = QFormLayout()
        self.collection_counter = QLabel()
        self.delivery_counter = QLabel()
        counter_layout.addRow("Collection", self.collection_counter)
        counter_layout.addRow("Delivery", self.delivery_counter)
        return counter_layout

    def setup_order_total_price(self):
        order_total_price_layout = QHBoxLayout()
        font1 = QFont()
        font1.setPointSize(14)
        self.total_price_label = QLabel('0.00')
        self.total_price_label.setFont(font1)
        order_total_price_layout.addWidget(QLabel("Total Price: "))
        order_total_price_layout.addWidget(QLabel("£ "))
        order_total_price_layout.addWidget(self.total_price_label)
        return order_total_price_layout



    def build_dish_suggestion_table(self):
        food_order_table = QTableWidget()
        column_names = ['No.', 'Dish', '食品', 'Price']

        food_order_table.setColumnCount(len(column_names))
        food_order_table.setRowCount(0)

        food_order_table.setHorizontalHeaderLabels(column_names)
        food_order_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return food_order_table
        
    ###
    #  Contact Form related UI
    ###
    def build_contact_form(self):
        form_layout = QFormLayout()

        # Create QLineEdit widgets for each form field
        self.phone_number_input = QLineEdit(self)
        self.name_input = QLineEdit(self)
        self.postcode_input = QLineEdit(self)
        self.address1_input = QLineEdit(self)
        self.address2_input = QLineEdit(self)
        self.customer_notes_input = QTextEdit(self)

        self.customer_notes_input.setMaximumHeight(150)

        # Add the widgets to the form layout
        form_layout.addRow("Phone No:", self.phone_number_input)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Postcode:", self.postcode_input)
        form_layout.addRow("Address: ", self.address1_input)
        form_layout.addRow("", self.address2_input)
        form_layout.addRow("Notes", self.customer_notes_input)


        self.phone_number_input.returnPressed.connect(self.handle_phone_number_enter)

        return form_layout
    
    def handle_phone_number_enter(self):
        if self.phone_number_input.text() != "":
            customer = CustomerUseCases().get_contact(self.phone_number_input.text())
            if customer is not None:
                self.populate_form(customer)
            else:
                self.clear_contact_form()
    
    def clear_contact_form(self):
        self.phone_number_input.clear()
        self.name_input.clear()
        self.postcode_input.clear()
        self.address1_input.clear()
        self.address2_input.clear()
        self.customer_notes_input.clear()
    
    def populate_form(self, customer: Customer):
        self.phone_number_input.setText(customer.telephone)
        self.name_input.setText(customer.name)
        self.address1_input.setText(customer.address1)
        self.address2_input.setText(customer.address2)
        self.postcode_input.setText(customer.postcode)
        self.customer_notes_input.setText(customer.comments)

    def build_grid_selectors(self):
        button_layout = QHBoxLayout()

        cat_button = QPushButton("Categories")
        button2 = QPushButton("Edit Dish")
        options_button = QPushButton("Options")

        cat_button.clicked.connect(self.activate_cat_button)        
        options_button.clicked.connect(self.activate_options_button)        


        button_layout.addWidget(cat_button)
        button_layout.addWidget(button2)
        button_layout.addWidget(options_button)

        return button_layout

    def activate_cat_button(self):
        print("cat")
        self.grid_stacked_layout.setCurrentIndex(0)

    def activate_options_button(self):
        print("options")
        self.grid_stacked_layout.setCurrentIndex(1)
    
    def build_stacked_layout(self):
        stacked_layout = QStackedLayout()

        stacked_layout.addWidget(self.build_grid())
        stacked_layout.addWidget(self.build_options_grid())
        stacked_layout.addWidget(self.build_address_suggestion_table())
        
        stacked_layout.setCurrentIndex(0)

        return stacked_layout

    def build_grid(self):
        grid_layout = QGridLayout()
        size = QSize(33,100)
        num_col = 3
        for i, category in enumerate(CATEGORIES):
            column = i%num_col
            row = i / num_col
            checkbox = QPushButton(category)
            checkbox.setMinimumSize(size)
            grid_layout.addWidget(checkbox, row, column)
        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)
        return grid_widget
    
    def build_options_grid(self):
        grid_layout = QGridLayout()
        size = QSize(33,100)
        num_col = 3
        for i, category in enumerate(OPTIONS):
            column = i%num_col
            row = i / num_col
            checkbox = QPushButton(category)
            checkbox.setMinimumSize(size)
            grid_layout.addWidget(checkbox, row, column)
        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)
        return grid_widget
    
    def build_address_suggestion_table(self):
        address_suggestion_table = QTableWidget()
        column_names = ['Phone Number', 'Address', 'Name']

        address_suggestion_table.setColumnCount(len(column_names))
        address_suggestion_table.setRowCount(0)

        address_suggestion_table.setHorizontalHeaderLabels(column_names)
        address_suggestion_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        address_suggestion_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        address_suggestion_table.setSelectionMode(QAbstractItemView.NoSelection)
        return address_suggestion_table
    
    def handle_address_clicked(self):
        pass
    
    def handle_options_button(self):
        options_grid_layout = self.build_options_grid()
        self.grid = options_grid_layout
        self.other_stuff_layout.addLayout(self.grid)

