
from http import HTTPStatus
from http.client import HTTPConnection
import json
from xmlrpc.client import Boolean
from DriverFront.Driver import Driver
from datetime import date


class Association:

    def __init__(self, name, abriv) -> None:
        self.name = name
        self.associationAbriv = abriv
        self.associationNo = 0
        self.driversList = []

    def getAbriviation(self):
        return self.associationAbriv

    def getAssociationNo(self):
        return self.associationNo
    
    def getName(self):
        return self.name

    def getDrivers(self):
        return self.driversList

    def generateAssociationNo(self):
        today = date.today().strftime("%m%d%Y")
        self.associationNo = self.associationAbriv+today
    
    def addDriver(self, driver):
        defaultType = type(Driver("","","",0))
        if type(driver) != defaultType:
            print("Not a valid driver")
            print(f"{type(driver)} is not {defaultType}")
            return
        driver.setAssociation(self.getAssociationNo())
        self.driversList.append(driver)
    
    def addAuthentications(self, password) -> bool:
        passangerRequest = HTTPConnection("127.0.0.1", 6666)
        
        data = [[self.getAssociationNo(), password, 1]]

        for driver in self.getDrivers():
            data.append([driver.getUserName(), f"{driver.getDetails()[1][:2]}12345@", 2])

        data = json.dumps(data)

        passangerRequest.request("POST", f"/add$Authentication", \
        headers={"data": data})
        requestResponse = passangerRequest.getresponse() 
        print(requestResponse.headers["response"])
        if requestResponse.status != HTTPStatus.CREATED:
            return False

        return True



