from PyQt5.QtWidgets import *

from datetime import datetime

from DbDishInterface import *
from FoodOrderUseCases import FoodNotFoundException

class DishWindow(QDialog):

    ## UI Stuff
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
        self.dish_table = self.build_suggestion_table()
        
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addWidget(self.display_label)
        self.main_layout.addWidget(self.dish_table)
        self.setLayout(self.main_layout)
        
    def build_display_text(self):
        """ This is useful for have a small QTextLabel to show any error messages"""
        return QLabel(self)

    def build_dialog_buttons(self):
        # Create a QHBoxLayout for the buttons
        button_layout = QVBoxLayout()

        # Create QPushButton
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.handle_save_button_pressed)
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
        self.dish_number_input.textChanged.connect(self.handle_dish_number_change)

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
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        table_widget.cellDoubleClicked.connect(self.handle_dish_clicked)
        return table_widget
        
    # Handlers and Business Logic
    def handle_save_button_pressed(self):
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
            dish_to_save = Dish(self.dish_number_input.text(), self.price_input.text(), 1, self.dish_name_input.text(), self.dish_chinese_input.text())
            try:
                DbDish.create_dish(dish_to_save)
                self.display_label.setText("New Dish Created!")
                self.display_label.setStyleSheet("color: green;")
            except DuplicateFoodException:
                DbDish.update_dish(dish_to_save)
                self.display_label.setText("Dish Updated!")
                self.display_label.setStyleSheet("color: green;")
        else:
            self.display_label.setText(error)
            self.display_label.setStyleSheet("color: red;")




    def handle_dish_number_enter(self):
        if self.dish_number_input.text() != "":
            dishes = DbDish.retrieve_dishes_by_id(self.dish_number_input.text())
            if len(dishes) == 0:   # New food 
                print("Dish not found, creata new food on save")
            else:
                dish = dishes[0]
                self.set_dish_text_inputs(dish)

    def set_dish_text_inputs(self, dish: Dish):
        self.dish_number_input.setText(dish.id)
        self.dish_name_input.setText(dish.description)
        self.dish_chinese_input.setText(dish.description_chinese)
        self.price_input.setText(str(dish.unit_price))
    
    def handle_dish_number_change(self):
        # Refresh
        self.dish_table.setRowCount(0)
        self.display_label.setText("")

        if self.dish_number_input.text() != "":
            # retrieve autofill dishes by id
            dishes  = DbDish.retrieve_dishes_by_id(self.dish_number_input.text())
            # Populate table
            for dish in dishes:
                self.dish_table.insertRow(self.dish_table.rowCount())
                dish_to_display = (dish.id,
                                    dish.description,
                                    dish.description_chinese,
                                    dish.unit_price)
                
                for i in range(self.dish_table.columnCount()):
                    # Each column is individually populated
                    item = QTableWidgetItem(str(dish_to_display[i]) if dish_to_display[i] else "")
                    self.dish_table.setItem(self.dish_table.rowCount()-1, i, item)
                self.dish_table.scrollToBottom()
            # Set up the items so that it can be clicked on
        else:
            # reset_table
            pass

    def handle_dish_clicked(self, row, column):
        print(f' row: {str(row)}, column {str(column)}')
        id = self.dish_table.item(row, 0).text()
        description = self.dish_table.item(row, 1).text()
        chinese = self.dish_table.item(row, 2).text()
        price = self.dish_table.item(row, 3).text()
        dish = Dish(id, price, 1, description, chinese)
        self.set_dish_text_inputs(dish)

    def handle_chinese_clicked(self):
        # Bring up a display (grid) of chinese characters
        
        # When clicked, add onto the self.dish_chinese_input value.
        pass