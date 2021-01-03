from PyQt5 import QtCore, QtGui, QtWidgets

from DbOrdersInterface import DbOrders

from datetime import datetime

class SummaryWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SummaryWindow, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.populate_table()

    def setupUi(self, Dialog):
        if Dialog.objectName():
            Dialog.setObjectName(u"Summary")
        Dialog.resize(604, 614)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QtCore.QRect(240, 570, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QtCore.QRect(190, 530, 211, 41))
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.grandTotalLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.grandTotalLabel.setObjectName(u"grandTotalLabel")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.grandTotalLabel.setFont(font)

        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.grandTotalLabel)

        self.grandTotalDisplayLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.grandTotalDisplayLabel.setObjectName(u"grandTotalDisplayLabel")
        font1 = QtGui.QFont()
        font1.setPointSize(16)
        self.grandTotalDisplayLabel.setFont(font1)
        self.grandTotalDisplayLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.grandTotalDisplayLabel)

        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)        
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QtCore.QRect(40, 60, 521, 461))
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)

        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.addItems(["Today", "This Month", "This Year"])
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QtCore.QRect(440, 30, 111, 21))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Summary")
        self.grandTotalLabel.setText("Grand Total: £")
        self.grandTotalDisplayLabel.setText("")

        header = self.tableWidget.horizontalHeader()
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText("No.")
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText("Qty")
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText("Dishes")
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText("Chinese")
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)        
    # retranslateUi

    def add_row(self, summary_food_item):
        if summary_food_item is not None:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            summary_food_item_display = (summary_food_item.item_number,
                                    summary_food_item.quantity,
                                    summary_food_item.description,
                                    summary_food_item.description_chinese)
            for i in range(self.tableWidget.columnCount()):
                item = QtWidgets.QTableWidgetItem(
                    str(summary_food_item_display[i]) if summary_food_item_display[i] else "")
                self.tableWidget.setItem(
                    self.tableWidget.rowCount()-1, i, item)
            self.tableWidget.scrollToBottom()

    def populate_table(self):
        # TODO: Populate Table based on date range.
        date_to_search = datetime.now().date()
        self.grandTotalDisplayLabel.setText(str(DbOrders.retrieve_total_price_by_date(date_to_search)))
        food_item_to_qty = DbOrders.retrieve_food_items_and_qty_by_date(date_to_search)
        for row in food_item_to_qty.values():
            self.add_row(row)

        
