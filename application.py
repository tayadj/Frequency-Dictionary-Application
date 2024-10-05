from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from collections import Counter
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


class QUserConfirmDialog(QDialog):

    label                       = None
    confirm                     = None

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Input")
        self.setFixedSize(240,120)

        self.label = QLabel(self)
        self.label.setGeometry(20, 20, 200, 30)
        self.label.setFont(QFont("Segoe UI Black",10))
        self.label.setText("Are you sure?")
        self.label.setAlignment(Qt.AlignCenter)

        self.confirm = QPushButton(self)
        self.confirm.clicked.connect(self.accept)
        self.confirm.setText("Confirm")
        self.confirm.setObjectName("confirm")
        self.confirm.setGeometry(80, 70, 80, 30)
        self.confirm.setFont(QFont("Segoe UI Black",10))
        self.confirm.setStyleSheet("#confirm:hover {"
                                   "    background-color: #f8f8f8;"
                                   "}")


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
    viewEditInput               = None
    viewEditConfirm             = None
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
            case 1027:
                print("Already exist")
            case _:
                print("Unknown error")

    def fillDictionary(self, data):

        self.viewViewDictionary.clear()
        self.viewViewDictionary.setRowCount(0)
        self.viewViewDictionary.setSortingEnabled(False)
        self.viewViewDictionary.show()
        self.viewViewDictionary.setRowCount(data.shape[0])
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
                self.dictionary = pandas.read_csv("./dict/dict_en.csv")
            case 2:
                self.dictionary = pandas.read_csv("./dict/dict_es.csv")
            case 3:
                self.dictionary = pandas.read_csv("./dict/dict_ru.csv")
            case _:
                self.errorMessage(1025)


    def uploadDictionary(self):

        match self.language:
            case 1:
                self.dictionary.to_csv('./dict/dict_en.csv', index=False)
            case 2:
                self.dictionary.to_csv('./dict/dict_es.csv', index=False)
            case 3:
                self.dictionary.to_csv('./dict/dict_ru.csv', index=False)
            case _:
                self.errorMessage(1025)

    def contextMenuEvent(self, event):

        contextMenu = QMenu(self)

        if self.viewView.isVisible():

            actionAdd = QAction("Add", self)
            actionAdd.triggered.connect(self.vieView_contextMenuActionAdd)
            contextMenu.addAction(actionAdd)

        if self.viewView.isVisible() and len(self.viewViewDictionary.selectedItems()) >= 1:

            actionDelete = QAction("Delete", self)
            actionDelete.triggered.connect(self.viewView_contextMenuActionDelete)
            contextMenu.addAction(actionDelete)

        if self.viewView.isVisible() and len(self.viewViewDictionary.selectedItems()) == 1:

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

    def viewView_contextMenuActionDelete(self):

        dialogue = QUserConfirmDialog(self)
        if dialogue.exec():
            for currentItem in self.viewViewDictionary.selectedItems():
                value = self.viewViewDictionary.item(currentItem.row(), 0).text()
                self.dictionary = self.dictionary[self.dictionary['Word'] != value]
            self.fillDictionary(self.dictionary)
            self.uploadDictionary()

    def vieView_contextMenuActionAdd(self):

        dialogue = QUserInputDialog(self)
        if dialogue.exec():
            newValue = dialogue.getValue().lower()
            if newValue in self.dictionary.values:
                self.errorMessage(1027)
            else:
                self.dictionary.loc[len(self.dictionary)] = {'Word': newValue, 'Frequency': 0}
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

    def clicked_viewEditConfirm(self):

        match self.language:
            case 1:
                with open("./txt_en/text0.txt", "a", encoding="utf-8") as file:
                    file.write(self.viewEditInput.toPlainText() + "\n\n\n\n\n")
                self.viewEditInput.setText("")

                texts = []
                for filename in os.listdir("./txt_en"):
                    if filename.endswith('.txt'):
                        with open(os.path.join("./txt_en", filename), 'r', encoding="utf-8") as file:
                            texts.append(file.read())

                all_words = []
                for text in texts:
                    text = text.lower()
                    text = re.sub(r'[^a-z\'-]', ' ', text)
                    words = text.split()
                    all_words.extend(words)
                frequency_dict = Counter(all_words)

                sorted_items = sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)
                with open("./dict/dict_en.csv", 'w', newline='', encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Word', 'Frequency'])
                    for word, freq in sorted_items:
                        writer.writerow([word, freq])

            case 2:
                with open("./txt_es/text0.txt", "a", encoding="utf-8") as file:
                    file.write(self.viewEditInput.toPlainText() + "\n\n\n\n\n")
                self.viewEditInput.setText("")

                texts = []
                for filename in os.listdir("./txt_es"):
                    if filename.endswith('.txt'):
                        with open(os.path.join("./txt_es", filename), 'r', encoding="utf-8") as file:
                            texts.append(file.read())

                all_words = []
                for text in texts:
                    text = text.lower()
                    text = re.sub(r'[^a-zёñáéíóúü\'-]', ' ', text)
                    words = text.split()
                    all_words.extend(words)
                frequency_dict = Counter(all_words)

                sorted_items = sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)
                with open("./dict/dict_es.csv", 'w', newline='', encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Word', 'Frequency'])
                    for word, freq in sorted_items:
                        writer.writerow([word, freq])

            case 3:
                with open("./txt_ru/text0.txt", "a", encoding="utf-8") as file:
                    file.write(self.viewEditInput.toPlainText() + "\n\n\n\n\n")
                self.viewEditInput.setText("")

                texts = []
                for filename in os.listdir("./txt_ru"):
                    if filename.endswith('.txt'):
                        with open(os.path.join("./txt_ru", filename), 'r', encoding="utf-8") as file:
                            texts.append(file.read())

                all_words = []
                for text in texts:
                    text = text.lower()
                    text = re.sub(r'[^а-я]', ' ', text)
                    words = text.split()
                    all_words.extend(words)
                frequency_dict = Counter(all_words)

                sorted_items = sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)
                with open("./dict/dict_ru.csv", 'w', newline='', encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Word', 'Frequency'])
                    for word, freq in sorted_items:
                        writer.writerow([word, freq])

            case _:
                self.errorMessage(1025)


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
        self.viewViewSearch.setFont(QFont("Segoe UI",8))
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

        self.viewEditInput = QTextEdit(self.viewEdit)
        self.viewEditInput.setObjectName("vieEditInput")
        self.viewEditInput.setGeometry(20, 20, 380, 200)
        self.viewEditInput.setFont(QFont("Segoe UI",8))
        self.viewEditInput.setStyleSheet("#vieEditInput {"
                                         "   border-radius: 10px;"
                                         "   background-color: #ffffff;"
                                         "}")

        self.viewEditConfirm = QPushButton(self.viewEdit)
        self.viewEditConfirm.clicked.connect(self.clicked_viewEditConfirm)
        self.viewEditConfirm.setObjectName("viewEditConfirm")
        self.viewEditConfirm.setText("CONFIRM")
        self.viewEditConfirm.setFont(QFont("Segoe UI Black",8))
        self.viewEditConfirm.setGeometry(160, 240, 100, 32)
        self.viewEditConfirm.setStyleSheet("#viewEditConfirm {"
                                           "    border-radius: 10px;"
                                           "    background-color: #f8f8f8;"
                                           "}"
                                           "#viewEditConfirm:hover {"
                                           "    background-color: #ffffff;"
                                           "}")

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

