from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QHBoxLayout, QPushButton, QLabel, QDialog, QLineEdit

from datetime import datetime


class DishWindow(QDialog):


    def __init__(self, parent=None):
        super().__init__(parent)        
        self.setWindowTitle("Edit Dish")

        self.main_layout = QVBoxLayout()

        self.input_layout = QHBoxLayout()
        form_layout = self.build_dish_input_form()
        button_layout = self.build_dialog_buttons()
        self.input_layout.addLayout(form_layout)
        self.input_layout.addLayout(button_layout)

        self.main_layout.addLayout(self.input_layout)
        self.setLayout(self.main_layout)


    def build_dialog_buttons(self):
        # Create a QHBoxLayout for the buttons
        button_layout = QVBoxLayout()

        # Create QPushButton for saving and canceling
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.accept)  # accept() closes the dialog and returns QDialog.Accepted
        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)  # reject() closes the dialog and returns QDialog.Rejected

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
        return form_layout

        
    def handle_save_dish(self):
        pass
