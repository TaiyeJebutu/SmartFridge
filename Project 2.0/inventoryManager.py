import json

class dataBase:



    # Initlisation of the dataBase class
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = False
        self.formatData = False

    # Reads the data in the database
    def readRecords(self):
        with open(self.filepath) as json_file:
            self.data = json.loads(json_file.read())
        json_file.close()
        self.dataFormat(self.data)

    # Prettifies the data from the database
    def dataFormat(self, data):
        self.formatData = json.dumps(data, indent=4)

    # Returns the data from the json file
    def outData(self):
        if self.data != False:
            return self.data
        else:
            raise Exception("No data has been loaded")

    # Returns the formatted data from the json file
    def outDataFormat(self):
        if self.formatData != False:
            return self.formatData
        else:
            raise Exception("No data has been loaded")

    # Adds new data to the Json file
    def addRecord(self, entry):
        if not self.doesItemExist(entry):
            with open(self.filepath, 'r+') as file:
                data = json.load(file)
                data["inventory"].append(entry)
                file.seek(0)
                json.dump(data, file, indent=4)
            file.close()
            return True
        else:
            return False

    # Updates data in json file
    def updateRecord(self, entry):
        if self.doesItemExist(entry):
            self.readRecords()
            data = self.data
            for dict in data["inventory"]:
                if dict["barcode"] == entry["barcode"]:
                    index = data["inventory"].index(dict)
                    data["inventory"][index] = entry
                    break
            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            file.close()
            self.readRecords()

    # Deletes data from the json file
    def deleteRecord(self,barcode):
        data = self.data
        for dict in data["inventory"]:
            if dict["barcode"] == barcode:
                index = data["inventory"].index(dict)
                break
        data["inventory"].pop(index)
        with open(self.filepath, "w") as file:
            json.dump(data, file)
        file.close()
        self.readRecords()

    # Checks if item exists
    def doesItemExist(self, entry):
        with open(self.filepath, 'r+') as file:
            data = json.load(file)
            exist = False
            for dict in data["inventory"]:
                if "barcode" in dict:
                    if dict["barcode"] == entry["barcode"]:
                        exist = True
        file.close()
        return exist
    # Gets an Item based of the barcode
    def getItemWithBarcode(self,barcode):
        entry = {"barcode": barcode}
        if self.doesItemExist(entry):
            data = self.data
            for dict in data["inventory"]:
                if "barcode" in dict:
                    if dict["barcode"] == entry["barcode"]:
                        break
            return dict
        else:
            return False

    # Gets an Item based of the name
    def getItemWithName(self, name):
        data = self.data
        unsortedNameDict = {}
        nameArray = []
        
        for dict in data["inventory"]:
            record = dict['name']
            if name.lower() in dict['name'].lower():
                unsortedNameDict[dict['name']] = dict['barcode']
                nameArray.append(dict['name'])
                

        if len(nameArray) > 1:
            nameArray.sort()
        
        sortedNameDict = [self.getItemWithBarcode(unsortedNameDict[names]) for names in nameArray ]
        return sortedNameDict

    #def get an Item based on calories
    def getItemWithCalories(self, minCal, maxCal):
        data = self.data
        result = []
        for dict in data['inventory']:
            if dict['calories'] <= maxCal and dict['calories'] >= minCal:
                result.append(dict)
        return result
        

    #Gets Attributes
    def getAttributes(self,attribute = None, barcode = ''):
        if attribute == 'item':
            item = self.getItemWithBarcode(barcode)['item']
            return item
        elif attribute == 'calories':
            item = self.getItemWithBarcode(barcode)['calories']
            return item
        elif attribute =='amount':
            item = self.getItemWithBarcode(barcode)['amount']
            return item
        elif attribute =='protein':
            item = self.getItemWithBarcode(barcode)['protein']
            return item
        elif attribute =='fats':
            item = self.getItemWithBarcode(barcode)['fats']
            return item
        elif attribute =='sugars':
            item = self.getItemWithBarcode(barcode)['sugars']
            return item
        elif attribute =='salts':
            item = self.getItemWithBarcode(barcode)['salts']
            return item
        else:
            return False














inventory = dataBase('inventory.txt')
inventory.readRecords()
print(inventory.outData())




