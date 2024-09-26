from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import pandas
import sys





class Window(QMainWindow):

    language        = 3
    dictionary      = None

    menu            = None
    menuView        = None
    menuEdit        = None
    menuSettings    = None
    view            = None
    viewDictionary  = None
    viewSettings    = None



    def errorMessage(self, error):
        print("Error " + str(error)+":")
        match error:
            case 101:
                print("Unknown language")
            case _:
                print("Unknown error")

    def fillViewDictionary(self):
        self.viewDictionary.clear()
        self.viewDictionary.show()
        self.viewDictionary.setRowCount(self.dictionary.shape[0])
        self.viewDictionary.setHorizontalHeaderItem(0, QTableWidgetItem("Wordform"))
        self.viewDictionary.setHorizontalHeaderItem(1, QTableWidgetItem("Frequency"))
        self.viewDictionary.horizontalHeaderItem(0).setFont(QFont("Segoe UI Black",8))
        self.viewDictionary.horizontalHeaderItem(1).setFont(QFont("Segoe UI Black",8))
        for i in range(self.dictionary.shape[0]):
            self.viewDictionary.setItem(i,0, QTableWidgetItem(str(self.dictionary.iat[i,0])))
            self.viewDictionary.setItem(i,1, QTableWidgetItem(str(self.dictionary.iat[i,1])))

    def loadDictionary(self):
        match self.language:
            case 1:
                self.dictionary = pandas.read_csv("../dict_en.csv")
            case 2:
                self.dictionary = pandas.read_csv("../dict_es.csv")
            case 3:
                self.dictionary = pandas.read_csv("../dict_ru.csv")
            case _:
                self.errorMessage(101)

    def clicked_menuView(self):
        self.viewDictionary.show()
        self.viewSettings.hide()
        self.loadDictionary()
        self.fillViewDictionary()

    def clicked_menuSettings(self):
        self.viewDictionary.hide()
        self.viewSettings.show()

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setFixedSize(720, 540)
        self.setWindowTitle("Application")

        self.menu = QGroupBox(self)
        self.menu.setGeometry(20, 20, 200, 500)
        self.menu.setStyleSheet("border-radius: 10px;");

        self.menuView = QPushButton(self.menu)
        self.menuView.clicked.connect(self.clicked_menuView)
        self.menuView.setObjectName("menuView")
        self.menuView.setText("VIEW")
        self.menuView.setFont(QFont("Segoe UI Black",12))
        self.menuView.setGeometry(20, 20, 160, 40)
        self.menuView.setStyleSheet("#menuView:hover {"
                                    "    background-color: #f8f8f8;"
                                    "}")

        self.menuEdit = QPushButton(self.menu)
        self.menuEdit.setObjectName("menuEdit")
        self.menuEdit.setText("EDIT")
        self.menuEdit.setFont(QFont("Segoe UI Black",12))
        self.menuEdit.setGeometry(20, 80, 160, 40)
        self.menuEdit.setStyleSheet("#menuEdit:hover {"
                                    "    background-color: #f8f8f8;"
                                    "}")

        self.menuSettings = QPushButton(self.menu)
        self.menuSettings.clicked.connect(self.clicked_menuSettings)
        self.menuSettings.setObjectName("menuSettings")
        self.menuSettings.setText("SETTINGS")
        self.menuSettings.setFont(QFont("Segoe UI Black",12))
        self.menuSettings.setGeometry(20, 140, 160, 40)
        self.menuSettings.setStyleSheet("#menuSettings:hover {"
                                        "    background-color: #f8f8f8;"
                                        "}")

        self.view = QGroupBox(self)
        self.view.setGeometry(240, 20, 460, 500)

        self.viewDictionary = QTableWidget(self.view)
        self.viewDictionary.setObjectName("viewDictionary")
        self.viewDictionary.setGeometry(20, 20, 420, 460)
        self.viewDictionary.setColumnCount(2);
        self.viewDictionary.setColumnWidth(0, 205)
        self.viewDictionary.setColumnWidth(1, 205)
        self.viewDictionary.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.viewDictionary.verticalHeader().setVisible(False)
        self.viewDictionary.hide()

        self.viewSettings = QGroupBox(self.view)
        self.viewSettings.setObjectName("viewSettings")
        self.viewSettings.setGeometry(20, 20, 420, 460)
        self.viewSettings.hide()


















if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

