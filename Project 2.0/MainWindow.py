import sys
from texttable import Texttable
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import time
from SmartFridge_Test3 import Ui_MainWindow
from inventoryManager import dataBase
import smtplib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer, Qt, QSize
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime
import requests
import json
from requests_html import HTMLSession
import re

from inventoryManager import dataBase

#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'nutrition.maestro.notify@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = 'wkdhqnmifihevczm'  #change this to match your gmail app-password

class MainWindow:

    def __init__(self):

        self.selectedTextBox = None
        self.Main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.Main_win)


        self.ui.stackedWidget.setCurrentWidget(self.ui.Home)
        # region original connect
        self.ui.ViewInventory.clicked.connect(self.showInventory)
        self.ui.RemoveAnItem.clicked.connect(self.showAddItem)
        self.ui.EditAnItem.clicked.connect(self.showRecipes)
        self.ui.ReturnHome.clicked.connect(self.showHome)
        self.ui.ReturnHome_2.clicked.connect(self.showHome)
        self.ui.ReturnHome_3.clicked.connect(self.showHome)
        self.ui.ReturnHome_7.clicked.connect(self.showHome)
        self.ui.ReturnHome_8.clicked.connect(self.showHome)
        self.ui.ReturnHome_9.clicked.connect(self.showHome)
        self.ui.ReturnHome_10.clicked.connect(self.ClearRecipe)
        self.ui.WithBarcode_2.clicked.connect(self.showBarcode_Add)
        self.ui.WithoutBarcode_2.clicked.connect(self.showNoBarcode_Add)
        self.ui.addNutritionalDataButton.clicked.connect(self.showNutrition)
        self.ui.PreviousScreen.clicked.connect(self.showNoBarcode_Add)
        self.ui.Submit.clicked.connect(self.    SaveAdd)
        self.ui.Submit_2.clicked.connect(self.SaveAdd)
        self.ui.Submit_3.clicked.connect(self.searchDatabase)
        self.ui.WithBarcode.clicked.connect(self.showRemoveWithBarcode)
        self.ui.Submit_4.clicked.connect(self.RemoveBarcodeSearch)
        self.ui.Submit_5.clicked.connect(self.RemoveBarcode)
        self.ui.sendEmail.clicked.connect(self.sendEmail)
        # endregion
        # region new connects
        self.ui.buttonSelectBarcodeOnEdit.clicked.connect(lambda: self.selectATextBox("EditBarcode"))
        self.ui.buttonSelectNameOnEdit.clicked.connect(lambda: self.selectATextBox("EditName"))
        self.ui.buttonSelectAmountOnEdit.clicked.connect(lambda: self.selectATextBox("EditAmount"))
        self.ui.buttonSelectUseByDateOnEdit.clicked.connect(lambda: self.selectATextBox("EditUseByDate"))
        self.ui.buttonSelectCaloriesOnPage.clicked.connect(lambda: self.selectATextBox("EditCalories"))
        self.ui.buttonSelectFatsOnPage.clicked.connect(lambda: self.selectATextBox("EditFats"))
        self.ui.buttonSelectSugarsOnPage.clicked.connect(lambda: self.selectATextBox("EditSugars"))
        self.ui.buttonSelectSaltsOnPage.clicked.connect(lambda: self.selectATextBox("EditSalts"))
        self.ui.buttonSelectProteinOnPage.clicked.connect(lambda: self.selectATextBox("EditProteins"))

        self.ui.buttonSelectBarcodeOnBarcode.clicked.connect(lambda: self.selectATextBox("Barcode"))

        self.ui.buttonClearEdit.clicked.connect(lambda: self.clearTextBox(self.selectedTextBox))
        self.ui.buttonClearPage.clicked.connect(lambda: self.clearTextBox(self.selectedTextBox))
        self.ui.buttonClearBarcode.clicked.connect(lambda: self.clearTextBox(self.selectedTextBox))

        #Recipes page Buttons
        self.ui.Omelette.clicked.connect(self.OmeletteRecipe)
        self.ui.PastaBake.clicked.connect(self.PastaBakeRecipe)



        self.ui.button0Edit.clicked.connect(lambda: self.textInput("0", self.selectedTextBox))
        self.ui.button1Edit.clicked.connect(lambda: self.textInput("1", self.selectedTextBox))
        self.ui.button2Edit.clicked.connect(lambda: self.textInput("2", self.selectedTextBox))
        self.ui.button3Edit.clicked.connect(lambda: self.textInput("3", self.selectedTextBox))
        self.ui.button4Edit.clicked.connect(lambda: self.textInput("4", self.selectedTextBox))
        self.ui.button5Edit.clicked.connect(lambda: self.textInput("5", self.selectedTextBox))
        self.ui.button6Edit.clicked.connect(lambda: self.textInput("6", self.selectedTextBox))
        self.ui.button7Edit.clicked.connect(lambda: self.textInput("7", self.selectedTextBox))
        self.ui.button8Edit.clicked.connect(lambda: self.textInput("8", self.selectedTextBox))
        self.ui.button9Edit.clicked.connect(lambda: self.textInput("9", self.selectedTextBox))

        self.ui.button0Page.clicked.connect(lambda: self.textInput("0", self.selectedTextBox))
        self.ui.button1Page.clicked.connect(lambda: self.textInput("1", self.selectedTextBox))
        self.ui.button2Page.clicked.connect(lambda: self.textInput("2", self.selectedTextBox))
        self.ui.button3Page.clicked.connect(lambda: self.textInput("3", self.selectedTextBox))
        self.ui.button4Page.clicked.connect(lambda: self.textInput("4", self.selectedTextBox))
        self.ui.button5Page.clicked.connect(lambda: self.textInput("5", self.selectedTextBox))
        self.ui.button6Page.clicked.connect(lambda: self.textInput("6", self.selectedTextBox))
        self.ui.button7Page.clicked.connect(lambda: self.textInput("7", self.selectedTextBox))
        self.ui.button8Page.clicked.connect(lambda: self.textInput("8", self.selectedTextBox))
        self.ui.button9Page.clicked.connect(lambda: self.textInput("9", self.selectedTextBox))

        self.ui.buttonQEdit.clicked.connect(lambda: self.textInput("Q", self.selectedTextBox))
        self.ui.buttonWEdit.clicked.connect(lambda: self.textInput("W", self.selectedTextBox))
        self.ui.buttonEEdit.clicked.connect(lambda: self.textInput("E", self.selectedTextBox))
        self.ui.buttonREdit.clicked.connect(lambda: self.textInput("R", self.selectedTextBox))
        self.ui.buttonTEdit.clicked.connect(lambda: self.textInput("T", self.selectedTextBox))
        self.ui.buttonYEdit.clicked.connect(lambda: self.textInput("Y", self.selectedTextBox))
        self.ui.buttonUEdit.clicked.connect(lambda: self.textInput("U", self.selectedTextBox))
        self.ui.buttonIEdit.clicked.connect(lambda: self.textInput("I", self.selectedTextBox))
        self.ui.buttonOEdit.clicked.connect(lambda: self.textInput("O", self.selectedTextBox))
        self.ui.buttonPEdit.clicked.connect(lambda: self.textInput("P", self.selectedTextBox))
        self.ui.buttonAEdit.clicked.connect(lambda: self.textInput("A", self.selectedTextBox))
        self.ui.buttonSEdit.clicked.connect(lambda: self.textInput("S", self.selectedTextBox))
        self.ui.buttonDEdit.clicked.connect(lambda: self.textInput("D", self.selectedTextBox))
        self.ui.buttonFEdit.clicked.connect(lambda: self.textInput("F", self.selectedTextBox))
        self.ui.buttonGEdit.clicked.connect(lambda: self.textInput("G", self.selectedTextBox))
        self.ui.buttonHEdit.clicked.connect(lambda: self.textInput("H", self.selectedTextBox))
        self.ui.buttonJEdit.clicked.connect(lambda: self.textInput("J", self.selectedTextBox))
        self.ui.buttonKEdit.clicked.connect(lambda: self.textInput("K", self.selectedTextBox))
        self.ui.buttonLEdit.clicked.connect(lambda: self.textInput("L", self.selectedTextBox))
        self.ui.buttonZEdit.clicked.connect(lambda: self.textInput("Z", self.selectedTextBox))
        self.ui.buttonXEdit.clicked.connect(lambda: self.textInput("X", self.selectedTextBox))
        self.ui.buttonCEdit.clicked.connect(lambda: self.textInput("C", self.selectedTextBox))
        self.ui.buttonVEdit.clicked.connect(lambda: self.textInput("V", self.selectedTextBox))
        self.ui.buttonBEdit.clicked.connect(lambda: self.textInput("B", self.selectedTextBox))
        self.ui.buttonNEdit.clicked.connect(lambda: self.textInput("N", self.selectedTextBox))
        self.ui.buttonMEdit.clicked.connect(lambda: self.textInput("M", self.selectedTextBox))
        self.ui.buttonSlashEdit.clicked.connect(lambda: self.textInput("/", self.selectedTextBox))

        self.ui.button0Barcode.clicked.connect(lambda: self.textInput("0", self.selectedTextBox))
        self.ui.button1Barcode.clicked.connect(lambda: self.textInput("1", self.selectedTextBox))
        self.ui.button2Barcode.clicked.connect(lambda: self.textInput("2", self.selectedTextBox))
        self.ui.button3Barcode.clicked.connect(lambda: self.textInput("3", self.selectedTextBox))
        self.ui.button4Barcode.clicked.connect(lambda: self.textInput("4", self.selectedTextBox))
        self.ui.button5Barcode.clicked.connect(lambda: self.textInput("5", self.selectedTextBox))
        self.ui.button6Barcode.clicked.connect(lambda: self.textInput("6", self.selectedTextBox))
        self.ui.button7Barcode.clicked.connect(lambda: self.textInput("7", self.selectedTextBox))
        self.ui.button8Barcode.clicked.connect(lambda: self.textInput("8", self.selectedTextBox))
        self.ui.button9Barcode.clicked.connect(lambda: self.textInput("9", self.selectedTextBox))

    def sendEmail(self):
        class Emailer:
            def sendmail(self, recipient, subject, content):
                # Create Headers
                headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                           "MIME-Version: 1.0", "Content-Type: text/html"]
                headers = "\r\n".join(headers)

                # Connect to Gmail Server
                session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                session.ehlo()
                session.starttls()
                session.ehlo()

                # Login to Gmail
                session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

                # Send Email & Exit
                session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
                session.quit

        sender = Emailer()

        inventory = dataBase('inventory.txt')
        inventory.readRecords()
        dictData = inventory.outData()
        content = Texttable()
        content.set_cols_dtype(["t", "t","t","t","t","t","t","t",])
        content.add_row(["Barcode","Name","Quantity","Calories","Proteins","Fats","Sugars","Salts"])

        trList = []

        def returnRecordsHTML(recordsList):
            message =''
            for records in recordsList:
                message = message +'<tr>'+ records+'</tr>'
            return message
        for record in dictData["inventory"]:
             print(record["barcode"])
             content.add_row([record["barcode"],record["item"],
                              record["amount"],record["calories"],
                              record["protein"],record["salts"],
                              record["sugars"],record["fats"]])

             trList.append(f'<td> {record["barcode"]}</td>'\
                           f'<td> {record["item"]}</td>'\
                           f'<td> {record["amount"]}</td>'\
                           f'<td> {record["calories"]}</td>'\
                           f'<td> {record["protein"]}</td>'\
                           f'<td> {record["salts"]}</td>'\
                           f'<td> {record["sugars"]}</td>'\
                           f'<td> {record["fats"]}</td>')

        htmlContent = (f'''
            <table>
            <thead>
              <tr>
                <th>Barcode</th>
                <th>Name</th>
                <th>Quantity</th>
                <th>Calories</th>
                <th>Proteins</th>
                <th>Fats</th>
                <th>Sugars</th>
                <th>Salts</th>
              </tr>
            </thead>
            <tbody>
              {returnRecordsHTML(trList)}
            </tbody>
            </table>''')
        string = "Hi there,\n"\
                 "\n\n\n"\
                 "Here are the items that you have:\n"\
                 f"{htmlContent}\n\n"\
                 "Have a lovely day\n"\
                 "Kind Regards,\nThe ImechE Team"











        sendTo = 'taiyejebutu@icloud.com'
        emailSubject = "Inventory Infomation"
        sender.sendmail(sendTo, emailSubject, string)
        print(htmlContent)
        print("Email Sent")


    def OmeletteRecipe(self):
        self.ui.Ingrediant1.setText("Egg")
        self.ui.Ingrediant2.setText("Ham")
        self.ui.QTY1.setText("2")
        self.ui.QTY2.setText("1")
        self.ui.QTYA1.setText("0")
        self.ui.QTYA2.setText("0")

    def PastaBakeRecipe(self):
        self.ui.Ingrediant1.setText("Pasta")
        self.ui.Ingrediant2.setText("Sauce")
        self.ui.Ingrediant3.setText("Chicken")
        self.ui.QTY1.setText("1 Cup")
        self.ui.QTY2.setText("1 Cup")
        self.ui.QTY3.setText("1 Breast")
        self.ui.QTYA1.setText("0")
        self.ui.QTYA2.setText("0")
        self.ui.QTYA3.setText("0")

    def ClearRecipe(self):
        self.ui.Ingrediant1.setText("")
        self.ui.Ingrediant2.setText("")
        self.ui.Ingrediant3.setText("")
        self.ui.QTY1.setText("")
        self.ui.QTY2.setText("")
        self.ui.QTY3.setText("")
        self.ui.QTYA1.setText("")
        self.ui.QTYA2.setText("")
        self.ui.QTYA3.setText("")
        self.showHome()


    def showRecipes(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Recipes)

        # endregion
    def clearTextBox(self, selectedTextBox):
        if (selectedTextBox == "EditBarcode"):
            self.ui.BarcodeInput_2.setText("")
        if (selectedTextBox == "EditName"):
            self.ui.NameOfFoodInput.setText("")
        if (selectedTextBox == "EditAmount"):
            self.ui.QuantityInput.setText("")
        if (selectedTextBox == "EditUseByDate"):
            self.ui.UseByDateInput.setText("")

        if (selectedTextBox == "EditCalories"):
            self.ui.CaloriesInput.setText("")
        if (selectedTextBox == "EditProteins"):
            self.ui.ProteinInput.setText("")
        if (selectedTextBox == "EditSalts"):
            self.ui.SaltsInput.setText("")
        if (selectedTextBox == "EditSugars"):
            self.ui.SugarsInput.setText("")
        if (selectedTextBox == "EditFats"):
            self.ui.FatsInput.setText("")

        if (selectedTextBox == "Barcode"):
            self.ui.BarcodeInput.setText("")

    def selectATextBox(self, selection):
        self.selectedTextBox = selection

    def textInput(self, text, selectedTextBox):
        if (selectedTextBox == "EditBarcode"):
            newtext = self.ui.BarcodeInput_2.text() + text
            self.ui.BarcodeInput_2.setText(newtext)
        if (selectedTextBox == "EditName"):
            newtext = self.ui.NameOfFoodInput.text() + text
            self.ui.NameOfFoodInput.setText(newtext)
        if (selectedTextBox == "EditAmount"):
            newtext = self.ui.QuantityInput.text() + text
            self.ui.QuantityInput.setText(newtext)
        if (selectedTextBox == "EditUseByDate"):
            newtext = self.ui.UseByDateInput.text() + text
            self.ui.UseByDateInput.setText(newtext)

        if (selectedTextBox == "EditCalories"):
            newtext = self.ui.CaloriesInput.text() + text
            self.ui.CaloriesInput.setText(newtext)
        if (selectedTextBox == "EditProteins"):
            newtext = self.ui.ProteinInput.text() + text
            self.ui.ProteinInput.setText(newtext)
        if (selectedTextBox == "EditSalts"):
            newtext = self.ui.SaltsInput.text() + text
            self.ui.SaltsInput.setText(newtext)
        if (selectedTextBox == "EditSugars"):
            newtext = self.ui.SugarsInput.text() + text
            self.ui.SugarsInput.setText(newtext)
        if (selectedTextBox == "EditFats"):
            newtext = self.ui.FatsInput.text() + text
            self.ui.FatsInput.setText(newtext)

        if (selectedTextBox == "Barcode"):
            newtext = self.ui.BarcodeInput.text() + text
            self.ui.BarcodeInput.setText(newtext)

    def show(self):
        self.Main_win.show()

    def showInventory(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Inventory)

    def showHome(self):
        self.clearAdd()
        self.ui.stackedWidget.setCurrentWidget(self.ui.Home)
        self.ui.HomePageInventory()
        self.ui.InventoryPageInventory()

    def showAddItem(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Add)

    def showRemoveItem(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Remove)

    def showRemoveWithBarcode(self):
        self.selectATextBox("Barcode")
        self.ui.stackedWidget.setCurrentWidget(self.ui.Barcode_Add)

    def showEditItem(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Edit)

    def showBarcode_Add(self):
        self.selectATextBox("Barcode")
        self.ui.stackedWidget.setCurrentWidget(self.ui.Barcode_Add)

    def searchDatabase(self):
        barcode = self.ui.BarcodeInput.text()
        inventory = dataBase('inventory.txt')
        inventory.readRecords()
        item = inventory.getItemWithBarcode(barcode)
        if (item != False):
            self.ui.BarcodeInput_2.setText(item['barcode'])
            self.ui.NameOfFoodInput.setText(item['item'])
            self.ui.QuantityInput.setText(item['amount'])
            self.ui.UseByDateInput.setText("not added")
            self.ui.CaloriesInput.setText(item['calories'])
            self.ui.ProteinInput.setText(item['protein'])
            self.ui.FatsInput.setText(item['fats'])
            self.ui.SugarsInput.setText(item['sugars'])
            self.ui.SaltsInput.setText(item['salts'])
            self.ui.BarcodeInput.setText("")
            self.showNoBarcode_Add()

    def RemoveBarcodeSearch(self):
        Barcode = self.ui.BarcodeInput_3.text()
        with open(r'InventoryDatabase.txt', 'r') as fp:
            # read all lines in a list
            lines = fp.readlines()
            for line in lines:
                # check if string present on a current line
                if ((line.find(Barcode) != -1) & (Barcode != "")):
                    print(Barcode, 'string exists in file')
                    print('Line Number:', lines.index(line))
                    print('Line:', line)
                    text = line
                    self.ui.RemoveCheck.setText(text)

        fp.close()

    def RemoveBarcode(self):
        Text = self.ui.RemoveCheck.text()
        print(Text.split(' | ')[0])

        with open("InventoryDatabase.txt", "r") as fp:
            lines = fp.readlines()
            lines.remove(Text)
        fp.close()

        with open("InventoryDatabase.txt", "w") as fp:
            fp.writelines(lines)
        fp.close()

    def showNoBarcode_Add(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.NoBarcode_Add)

    def showNutrition(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

    def SaveAdd(self):

        inventory = dataBase('inventory.txt')
        inventory.readRecords()

        barcode = self.ui.BarcodeInput_2.text()
        item = self.ui.NameOfFoodInput.text()
        quantity = self.ui.QuantityInput.text()
        useByDate = self.ui.UseByDateInput.text()
        calories = self.ui.CaloriesInput.text()
        protein = self.ui.ProteinInput.text()
        salts = self.ui.SaltsInput.text()
        sugars = self.ui.SugarsInput.text()
        fats = self.ui.FatsInput.text()

        record = {
            "barcode": barcode,
            "item": item,
            "amount": quantity,
            "calories": calories,
            "protein": protein,
            "salts": salts,
            "sugars": sugars,
            "fats": fats
        }

        inventory.updateRecord(record)
        self.clearAdd()
        self.refreshInventory()

    def clearAdd(self):
        self.ui.BarcodeInput_2.setText("")
        self.ui.NameOfFoodInput.setText("")
        self.ui.QuantityInput.setText("")
        self.ui.UseByDateInput.setText("")
        self.ui.CaloriesInput.setText("")
        self.ui.ProteinInput.setText("")
        self.ui.FatsInput.setText("")
        self.ui.SugarsInput.setText("")
        self.ui.SaltsInput.setText("")

    def refreshInventory(self):
        with open('InventoryDatabase.txt', 'r') as f:
            last_line = f.readlines()[-1]
        print(last_line)
        # object = QLabel(last_line)
        # self.ui.verticalLayout.addWidget(object)

        # with open('InventoryDatabase.txt') as f:
        # contents = f.read()
        # object = QLabel(contents)
        # self.verticalLayout.addWidget(object)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Main_win = MainWindow()
    Main_win.show()
    sys.exit(app.exec_())
