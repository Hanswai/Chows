from PyQt5.QtWidgets import QDialogButtonBox, QDialog, QVBoxLayout, QLabel


class NoActionDialog(QDialog):

    def __init__(self, food_id):
        super().__init__()

        self.setWindowTitle("Food Not Found")

        QBtn = QDialogButtonBox.Ok

        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        message = QLabel(f"""Number {food_id} is not on the menu. 
Please add a new item with Edit -> <This is not finished yet>
, or try another number.""")
        layout.addWidget(message)
        layout.addWidget(buttonBox)
        self.setLayout(layout)