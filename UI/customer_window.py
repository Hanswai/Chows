from PyQt5.QtWidgets import *
from DbDishInterface import *



class CustomerWindow(QDialog):

    ## UI Stuff
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Customer")

        form_layout = self.build_address_input_form()
        button_layout = self.build_dialog_buttons()

        self.input_layout = QHBoxLayout()
        self.input_layout.addLayout(form_layout)
        self.input_layout.addLayout(button_layout)

        self.display_label = self.build_display_text()
        self.customer_table = self.build_suggestion_table()

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addWidget(self.display_label)
        self.main_layout.addWidget(self.customer_table)
        self.setLayout(self.main_layout)
        
    def build_display_text(self):
        """ For showing any error messages"""
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

    
    def build_address_input_form(self):
        form_layout = QFormLayout()

        # Create QLineEdit widgets for each form field
        self.telephone_number_input = QLineEdit(self)
        self.address_1_input = QLineEdit(self)
        self.address_2_input = QLineEdit(self)

        self.postcode_input = QLineEdit(self)
        self.name_input = QLineEdit(self)
        self.notes_input = QLineEdit(self)

        # Add the widgets to the form layout
        form_layout.addRow("Phone Number", self.telephone_number_input)
        form_layout.addRow("Address", self.address_1_input)
        form_layout.addRow("Address 2", self.address_2_input)

        form_layout.addRow("Postcode", self.postcode_input)
        form_layout.addRow("Name", self.name_input)
        form_layout.addRow("Notes", self.notes_input)

        self.telephone_number_input.returnPressed.connect(self.handle_phone_number_enter)
        self.telephone_number_input.textChanged.connect(self.handle_phone_number_change)

        return form_layout

    def build_suggestion_table(self):
        table_widget = QTableWidget(self)

        column_names = ['Phone Number', 'Name', 'Address 1', 'Address 2', 'Postcode']
        table_widget.setColumnCount(len(column_names))
        table_widget.setRowCount(0)

        table_widget.setHorizontalHeaderLabels(column_names)
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        table_widget.cellDoubleClicked.connect(self.handle_dish_clicked)
        return table_widget
        
    # Handlers and Business Logic
    def handle_save_button_pressed(self):
        pass

    def handle_phone_number_enter(self):
        pass
    
    def handle_phone_number_change(self):
        # Refresh
        self.customer_table.setRowCount(0)
        self.display_label.setText("")

        if self.telephone_number_input.text() != "":
            pass

    def handle_dish_clicked(self, row, column):
        pass
