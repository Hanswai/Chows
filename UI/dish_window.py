from PyQt5.QtWidgets import *

from datetime import datetime

from DbDishInterface import *
from FoodOrderUseCases import FoodNotFoundException


class DishWindow(QDialog):


    def __init__(self, parent=None):
        super().__init__(parent)        
        self.setWindowTitle("Edit Dish")

        self.main_layout = QVBoxLayout()

        self.input_layout = QHBoxLayout()
        form_layout = self.build_dish_input_form()
        button_layout = self.build_dialog_buttons()
        category_layout = self.build_category_grid_input()
        self.input_layout.addLayout(form_layout)
        self.input_layout.addLayout(category_layout)
        self.input_layout.addLayout(button_layout)
        self.display_label = self.build_display_text()
        dish_table = self.build_suggestion_table()

        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addWidget(self.display_label)
        self.main_layout.addWidget(dish_table)
        self.setLayout(self.main_layout)
        
    def build_display_text(self):
        """ This is useful for have a small QTextLabel to show any error messages"""
        return QLabel(self)

    def build_dialog_buttons(self):
        # Create a QHBoxLayout for the buttons
        button_layout = QVBoxLayout()

        # Create QPushButton
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.handle_save_dish)
        save_button.setDefault(False)

        cancel_button = QPushButton("Close", self)
        cancel_button.setDefault(True)

        # Add buttons to the button layout
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        return button_layout

    
    def build_dish_input_form(self):
        form_layout = QFormLayout()

        # Create QLineEdit widgets for each form field
        self.dish_number_input = QLineEdit(self)
        self.dish_name_input = QLineEdit(self)
        self.dish_chinese_input = QLineEdit(self)
        self.price_input = QLineEdit(self)

        # Add the widgets to the form layout
        form_layout.addRow("Dish Number:", self.dish_number_input)
        form_layout.addRow("Dish Name:", self.dish_name_input)
        form_layout.addRow("Chinese Dish Name:", self.dish_chinese_input)
        form_layout.addRow("Price:", self.price_input)

        self.dish_number_input.returnPressed.connect(self.handle_dish_number_enter)
        return form_layout
    
    def build_category_grid_input(self):
        grid_layout = QGridLayout()

        num_col = 3
        categories = ['Appetisers','Beef', 'Chicken', 'Duck', 'Rice', 'Noodles', 'Soup']
        for i, category in enumerate(categories):
            column = i/num_col
            row = i % num_col
            checkbox = QCheckBox(self)
            checkbox.setText(category)
            grid_layout.addWidget(checkbox, row, column)
        return grid_layout

    def build_suggestion_table(self):
        table_widget = QTableWidget(self)

        table_widget.setColumnCount(4)
        table_widget.setRowCount(0)

        column_names = ['No.', 'Dish', '食品', 'Price']
        table_widget.setHorizontalHeaderLabels(column_names)
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return table_widget
        
    def handle_save_dish(self):
        # Check inputs

        # Send error message
        message = ""
        error = False
        if self.dish_number_input.text() == "":
            message += "Missing Dish Number. "
            error = True

        if self.dish_name_input.text() == "":
            message += "Missing Dish Name. "
            error = True

        if self.dish_chinese_input.text() == "":
            message += "Missing Chinese Dish Name. "
            error = True

        if self.price_input.text() == "":
            message += "Missing Price. "
            error = True

        try:
            float(self.price_input.text())
        except ValueError:
            message += "Price needs to be a number. (e.g. 10, 10.0, 10.50)"
            error = True
        
        if not error:
            self.display_label.setText(message if error else "Saving...")
            dish_to_save = Dish(self.dish_number_input.text, self.price_input.text, 1, self.dish_name_input.text, self.dish_chinese_input)
            DbDish.create_dish(dish_to_save)
            self.display_label.setText("Success!")



    def handle_dish_number_enter(self):
        if self.dish_number_input.text() != "":
            dishes = DbDish.retrieve_dishes_by_id(self.dish_number_input.text())
            if len(dishes) == 0:   # New food 
                print("Dish not found, creata new food on save")
            else:
                dish = dishes[0]
                self.dish_name_input.setText(dish.description)
                self.dish_chinese_input.setText(dish.description_chinese)
                self.price_input.setText(str(dish.unit_price))
            