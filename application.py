from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import pandas
import sys
import csv
import re
import os



class QNumericTableWidgetItem(QTableWidgetItem):

    def __lt__(self, other):

        if isinstance(other, QTableWidgetItem):
            try:
                return float(self.text()) < float(other.text())
            except ValueError:
                pass
        return super().__lt__(other)




class QUserInputDialog(QDialog):

    input                       = None
    submit                      = None

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Input")
        self.setFixedSize(240,120)

        self.input = QLineEdit(self)
        self.input.setGeometry(20, 20, 200, 30)
        self.input.setFont(QFont("Segoe UI",10))
        self.input.setPlaceholderText("Enter new value...")

        self.submit = QPushButton(self)
        self.submit.clicked.connect(self.accept)
        self.submit.setText("Submit")
        self.submit.setObjectName("submit")
        self.submit.setGeometry(80, 70, 80, 30)
        self.submit.setFont(QFont("Segoe UI Black",10))
        self.submit.setStyleSheet("#submit:hover {"
                                  "    background-color: #f8f8f8;"
                                  "}")


    def getValue(self):

        return self.input.text()




class Window(QMainWindow):

    language                    = 1
    dictionary                  = None
    regularExpression           = None

    menu                        = None
    menuView                    = None
    menuEdit                    = None
    menuSettings                = None
    view                        = None
    viewView                    = None
    viewViewDictionary          = None
    viewViewSearch              = None
    viewEdit                    = None
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

    def fillDictionary(self, data):

        self.viewViewDictionary.clear()
        self.viewViewDictionary.setRowCount(0)
        self.viewViewDictionary.setSortingEnabled(False)
        self.viewViewDictionary.show()
        self.viewViewDictionary.setRowCount(self.dictionary.shape[0])
        self.viewViewDictionary.setHorizontalHeaderItem(0, QTableWidgetItem("Word"))
        self.viewViewDictionary.setHorizontalHeaderItem(1, QTableWidgetItem("Frequency"))
        self.viewViewDictionary.horizontalHeaderItem(0).setFont(QFont("Segoe UI Black",8))
        self.viewViewDictionary.horizontalHeaderItem(1).setFont(QFont("Segoe UI Black",8))
        for i in range(data.shape[0]):
            self.viewViewDictionary.setItem(i,0, QTableWidgetItem(str(data.iat[i,0])))
            self.viewViewDictionary.setItem(i,1, QNumericTableWidgetItem(str(data.iat[i,1])))
        self.viewViewDictionary.setSortingEnabled(True)

    def downloadDictionary(self):

        match self.language:
            case 1:
                self.dictionary = pandas.read_csv("../dict_en.csv")
            case 2:
                self.dictionary = pandas.read_csv("../dict_es.csv")
            case 3:
                self.dictionary = pandas.read_csv("../dict_ru.csv")
            case _:
                self.errorMessage(1025)


    def uploadDictionary(self):

        match self.language:
            case 1:
                self.dictionary.to_csv('../dict_en.csv', index=False)
            case 2:
                self.dictionary.to_csv('../dict_es.csv', index=False)
            case 3:
                self.dictionary.to_csv('../dict_ru.csv', index=False)
            case _:
                self.errorMessage(1025)

    def contextMenuEvent(self, event):

        if self.viewView.isVisible() and len(self.viewViewDictionary.selectedItems()) == 1:
            contextMenu = QMenu(self)
            actionEdit = QAction("Edit", self)
            actionEdit.triggered.connect(self.viewView_contextMenuActionEdit)
            contextMenu.addAction(actionEdit)
            contextMenu.exec(event.globalPos())

    def viewView_contextMenuActionEdit(self):

        value = self.viewViewDictionary.item(self.viewViewDictionary.currentItem().row(), 0).text()
        dialogue = QUserInputDialog(self)
        if dialogue.exec():
            newValue = dialogue.getValue().lower()
            newFrequency = self.dictionary[self.dictionary['Word'] == value].Frequency.sum() + self.dictionary[self.dictionary['Word'] == newValue].Frequency.sum()
            self.dictionary = self.dictionary[self.dictionary['Word'] != value]
            self.dictionary = self.dictionary[self.dictionary['Word'] != newValue]
            self.dictionary.loc[len(self.dictionary)] = {'Word': newValue, 'Frequency': newFrequency}
            self.fillDictionary(self.dictionary)
            self.uploadDictionary()

    def clicked_menuView(self):

        self.viewView.show()
        self.viewEdit.hide()
        self.viewSettings.hide()
        self.downloadDictionary()
        self.fillDictionary(self.dictionary)

    def clicked_menuEdit(self):

        self.viewView.hide()
        self.viewEdit.show()
        self.viewSettings.hide()

    def clicked_menuSettings(self):

        self.viewView.hide()
        self.viewEdit.hide()
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

    def textChanged_viewViewSearch(self, text):

        if text == "":
            self.fillDictionary(self.dictionary)
        else:
            filteredDictionary = self.dictionary[self.dictionary['Word'].str.startswith(text) == True]
            self.fillDictionary(filteredDictionary)

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
        self.menuView.setFont(QFont("Segoe UI Black",16))
        self.menuView.setGeometry(20, 20, 160, 40)
        self.menuView.setStyleSheet("#menuView:hover {"
                                    "    background-color: #f8f8f8;"
                                    "}")

        self.menuEdit = QPushButton(self.menu)
        self.menuEdit.clicked.connect(self.clicked_menuEdit)
        self.menuEdit.setObjectName("menuEdit")
        self.menuEdit.setText("EDIT")
        self.menuEdit.setFont(QFont("Segoe UI Black",16))
        self.menuEdit.setGeometry(20, 80, 160, 40)
        self.menuEdit.setStyleSheet("#menuEdit:hover {"
                                    "    background-color: #f8f8f8;"
                                    "}")

        self.menuSettings = QPushButton(self.menu)
        self.menuSettings.clicked.connect(self.clicked_menuSettings)
        self.menuSettings.setObjectName("menuSettings")
        self.menuSettings.setText("SETTINGS")
        self.menuSettings.setFont(QFont("Segoe UI Black",16))
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

        self.viewView = QGroupBox(self.view)
        self.viewView.setObjectName("viewView")
        self.viewView.setGeometry(20, 20, 420, 460)
        self.viewView.setStyleSheet("#viewView {"
                                    "   border-radius: 10px;"
                                    "   background-color: #f8f8f8;"
                                    "}")
        self.viewView.hide()

        self.viewViewSearch = QLineEdit(self.viewView)
        self.viewViewSearch.setObjectName("viewViewSearch")
        self.viewViewSearch.setGeometry(20, 20, 380, 20)
        self.viewViewSearch.setPlaceholderText("Enter search pattern...")
        self.viewViewSearch.textChanged.connect(self.textChanged_viewViewSearch)

        self.viewViewDictionary = QTableWidget(self.viewView)
        self.viewViewDictionary.setObjectName("viewDictionary")
        self.viewViewDictionary.setGeometry(20, 60, 380, 380)
        self.viewViewDictionary.setColumnCount(2);
        self.viewViewDictionary.setColumnWidth(0, 183)
        self.viewViewDictionary.setColumnWidth(1, 183)
        self.viewViewDictionary.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.viewViewDictionary.verticalHeader().setVisible(False)
        self.viewViewDictionary.setSortingEnabled(True)
        self.viewViewDictionary.hide()

        self.viewEdit = QGroupBox(self.view)
        self.viewEdit.setObjectName("viewEdit")
        self.viewEdit.setGeometry(20, 20, 420, 460)
        self.viewEdit.setStyleSheet("#viewEdit {"
                                    "   border-radius: 10px;"
                                    "   background-color: #f8f8f8;"
                                    "}")
        self.viewEdit.hide()

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

