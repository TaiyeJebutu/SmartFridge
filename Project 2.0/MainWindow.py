import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import time
from SmartFridge_Test3 import Ui_MainWindow
from inventoryManager import dataBase

class MainWindow:
    def __init__(self):
        self.Main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.Main_win)

        self.ui.stackedWidget.setCurrentWidget(self.ui.Home)

        self.ui.ViewInventory.clicked.connect(self.showInventory)
        self.ui.AddItem.clicked.connect(self.showAddItem)



        self.ui.ReturnHome.clicked.connect(self.showHome)
        self.ui.ReturnHome_2.clicked.connect(self.showHome)
        self.ui.ReturnHome_3.clicked.connect(self.showHome)
        self.ui.ReturnHome_7.clicked.connect(self.showHome)
        self.ui.ReturnHome_8.clicked.connect(self.showHome)
        self.ui.ReturnHome_9.clicked.connect(self.showHome)
        self.ui.ReturnHome_10.clicked.connect(self.showHome)
        self.ui.WithBarcode_2.clicked.connect(self.showBarcode_Add)
        self.ui.WithoutBarcode_2.clicked.connect(self.showNoBarcode_Add)
        self.ui.addNutritionalDataButton.clicked.connect(self.showNutrition)
        self.ui.PreviousScreen.clicked.connect(self.showNoBarcode_Add)
        self.ui.Submit.clicked.connect(self.SaveAdd)
        self.ui.Submit_3.clicked.connect(self.searchDatabase)
        self.ui.RemoveAnItem.clicked.connect(self.showRemoveItem)
        self.ui.EditAnItem.clicked.connect(self.showEditItem)
        self.ui.WithBarcode.clicked.connect(self.showRemoveWithBarcode)
        self.ui.Submit_4.clicked.connect(self.RemoveBarcodeSearch)
        self.ui.Submit_5.clicked.connect(self.RemoveBarcode)

    def show(self):
        self.Main_win.show()

    def showInventory(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Inventory)
        #self.ui.InventoryPageInventory()

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
        self.ui.stackedWidget.setCurrentWidget(self.ui.Barcode_Rem)

    def showEditItem(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Edit)

    def showBarcode_Add(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Barcode_Add)

    def searchDatabase(self):
        barcode = self.ui.BarcodeInput.text()
        inventory = dataBase('inventory.txt')
        inventory.readRecords()
        item = inventory.getItemWithBarcode(barcode)
        if(item != False):
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
        useByDate= self.ui.UseByDateInput.text()
        calories= self.ui.CaloriesInput.text()
        protein= self.ui.ProteinInput.text()
        salts= self.ui.SaltsInput.text()
        sugars= self.ui.SugarsInput.text()
        fats= self.ui.FatsInput.text()

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


        """if (self.ui.BarcodeInput_2.text != ""):
            Barcode = self.ui.BarcodeInput_2.text()
        else:
            Barcode = ""
        if (self.ui.NameOfFoodInput.text != ""):
            Food = self.ui.NameOfFoodInput.text()
        else:
            Food = ""
        if (self.ui.QuantityInput.text != ""):
            Quantity = self.ui.QuantityInput.text()
        else:
            Quantity = ""
        if (self.ui.UseByDateInput.text != ""):
            UseByDate = self.ui.UseByDateInput.text()
        else:
            UseByDate = ""
        if (self.ui.CaloriesInput.text != ""):
            Calories = self.ui.CaloriesInput.text()
        else:
            Calories = ""
        if (self.ui.ProteinInput.text != ""):
            Protein = self.ui.ProteinInput.text()
        else:
            Protein = ""
        if (self.ui.SaltsInput.text != ""):
            Salts = self.ui.SaltsInput.text()
        else:
            Salts = ""
        if (self.ui.SugarsInput.text != ""):
            Sugars = self.ui.SugarsInput.text()
        else:
            Sugars = ""
        if (self.ui.FatsInput.text != ""):
            Fats = self.ui.FatsInput.text()
        else:
            Fats = ""

        f = open("InventoryDatabase.txt", "a")

        f.write("Barcode: " + Barcode + " | Item: " + Food + " | Amount: " + Quantity +
                " | Calories: " + Calories +
                " | Protein: " + Protein +
                " | Fats: " + Fats +
                " | Sugars: " + Sugars +
                " | Salts: " + Salts )

        f.close()
        self.clearAdd()
        self.refreshInventory()"""

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
        #object = QLabel(last_line)
        #self.ui.verticalLayout.addWidget(object)

        #with open('InventoryDatabase.txt') as f:
            #contents = f.read()
            #object = QLabel(contents)
            #self.verticalLayout.addWidget(object)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    Main_win = MainWindow()
    Main_win.show()
    sys.exit(app.exec_())
