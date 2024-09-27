from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import pandas
import sys


class QNumericTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        if isinstance(other, QTableWidgetItem):
            try:
                return float(self.text()) < float(other.text())
            except ValueError:
                pass
        return super().__lt__(other)





class Window(QMainWindow):

    language                    = 1
    dictionary                  = None

    menu                        = None
    menuView                    = None
    menuEdit                    = None
    menuSettings                = None
    view                        = None
    viewDictionary              = None
    viewSearch                  = None
    viewSettings                = None
    viewSettingsLanguageHeader  = None
    viewSettingsLanguageLine    = None
    viewSettingsLanguageOption  = None
    viewSettingsLanguageEnglish = None
    viewSettingsLanguageSpanish = None
    viewSettingsLanguageRussian = None




    def errorMessage(self, error):
        print("Error " + str(error)+":")
        match error:
            case 1025:
                print("Unknown language")
            case 1026:
                print("Setting language is wrong")
            case _:
                print("Unknown error")

    def fillViewDictionary(self):
        self.viewDictionary.clear()
        self.viewDictionary.setRowCount(0)
        self.viewDictionary.setSortingEnabled(False)
        self.viewDictionary.show()
        self.viewDictionary.setRowCount(self.dictionary.shape[0])
        self.viewDictionary.setHorizontalHeaderItem(0, QTableWidgetItem("Wordform"))
        self.viewDictionary.setHorizontalHeaderItem(1, QTableWidgetItem("Frequency"))
        self.viewDictionary.horizontalHeaderItem(0).setFont(QFont("Segoe UI Black",8))
        self.viewDictionary.horizontalHeaderItem(1).setFont(QFont("Segoe UI Black",8))
        for i in range(self.dictionary.shape[0]):
            self.viewDictionary.setItem(i,0, QTableWidgetItem(str(self.dictionary.iat[i,0])))
            self.viewDictionary.setItem(i,1, QNumericTableWidgetItem(str(self.dictionary.iat[i,1])))
        self.viewDictionary.setSortingEnabled(True)

    def loadDictionary(self):
        match self.language:
            case 1:
                self.dictionary = pandas.read_csv("../dict_en.csv")
            case 2:
                self.dictionary = pandas.read_csv("../dict_es.csv")
            case 3:
                self.dictionary = pandas.read_csv("../dict_ru.csv")
            case _:
                self.errorMessage(1025)

    def clicked_menuView(self):
        self.viewDictionary.show()
        self.viewSettings.hide()
        self.loadDictionary()
        self.fillViewDictionary()

    def clicked_menuSettings(self):
        self.viewDictionary.hide()
        self.viewSettings.show()

    def buttonClicked_viewSettingsLanguageOption(self, option):
        match option.text():
            case "ENGLISH":
                self.language = 1
            case "SPANISH":
                self.language = 2
            case "RUSSIAN":
                self.language = 3
            case _:
                self.errorMessage(1026)


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
        self.view.setObjectName("view")
        self.view.setGeometry(240, 20, 460, 500)
        self.view.setStyleSheet("#view {"
                                "   border: none;"
                                "}")

        self.viewDictionary = QTableWidget(self.view)
        self.viewDictionary.setObjectName("viewDictionary")
        self.viewDictionary.setGeometry(20, 20, 420, 460)
        self.viewDictionary.setColumnCount(2);
        self.viewDictionary.setColumnWidth(0, 203)
        self.viewDictionary.setColumnWidth(1, 203)
        self.viewDictionary.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.viewDictionary.verticalHeader().setVisible(False)
        self.viewDictionary.setSortingEnabled(True)
        self.viewDictionary.hide()

        self.viewSettings = QGroupBox(self.view)
        self.viewSettings.setObjectName("viewSettings")
        self.viewSettings.setGeometry(20, 20, 420, 460)
        self.viewSettings.setStyleSheet("#viewSettings {"
                                        "   border-radius: 10px;"
                                        "   background-color: #f8f8f8;"
                                        "}")
        self.viewSettings.hide()

        self.viewSettingsLanguageHeader = QLabel(self.viewSettings)
        self.viewSettingsLanguageHeader.setGeometry(20, 20, 120, 20)
        self.viewSettingsLanguageHeader.setFont(QFont("Segoe UI Black",12))
        self.viewSettingsLanguageHeader.setText("LANGUAGE")

        self.viewSettingsLanguageLine = QFrame(self.viewSettings)
        self.viewSettingsLanguageLine.setGeometry(20, 44, 380, 2)
        self.viewSettingsLanguageLine.setFrameShape(QFrame.HLine)
        self.viewSettingsLanguageLine.setFrameShadow(QFrame.Sunken)

        self.viewSettingsLanguageEnglish = QRadioButton(self.viewSettings, "English")
        self.viewSettingsLanguageEnglish.setGeometry(20, 60, 120, 20)
        self.viewSettingsLanguageEnglish.setFont(QFont("Segoe UI Black",10))
        self.viewSettingsLanguageEnglish.setText("ENGLISH")
        self.viewSettingsLanguageEnglish.setChecked(True)
        self.viewSettingsLanguageSpanish = QRadioButton(self.viewSettings, "Spanish")
        self.viewSettingsLanguageSpanish.setGeometry(20, 90, 120, 20)
        self.viewSettingsLanguageSpanish.setFont(QFont("Segoe UI Black",10))
        self.viewSettingsLanguageSpanish.setText("SPANISH")
        self.viewSettingsLanguageRussian = QRadioButton(self.viewSettings, "Russian")
        self.viewSettingsLanguageRussian.setGeometry(20, 120, 120, 20)
        self.viewSettingsLanguageRussian.setFont(QFont("Segoe UI Black",10))
        self.viewSettingsLanguageRussian.setText("RUSSIAN")

        self.viewSettingsLanguageOption = QButtonGroup(self.viewSettings)
        self.viewSettingsLanguageOption.addButton(self.viewSettingsLanguageEnglish)
        self.viewSettingsLanguageOption.addButton(self.viewSettingsLanguageSpanish)
        self.viewSettingsLanguageOption.addButton(self.viewSettingsLanguageRussian)
        self.viewSettingsLanguageOption.buttonClicked.connect(self.buttonClicked_viewSettingsLanguageOption)


















if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

