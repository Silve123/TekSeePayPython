import sqlite3
import DBMS

class HTTPAPI:
    """ Used to call the requred data from the database"""

    def __init__(self) -> None:
        self.connection = sqlite3.connect("testdatabase.db")

    def getDriver(self, id):
        return DBMS.DriverdatabaseManagement(self.connection).getDriver(id)

    def getAssociation(self, id):
        return DBMS.AssociationsdatabaseManagement(self.connection).getAssociation(id)
        
    def updateDriverStatus(self, id, status):
        return DBMS.DriverdatabaseManagement(self.connection).updateDriverStatus(id, status)
    
    def updateDriver(self, Driver):
        return DBMS.DriverdatabaseManagement(self.connection).updateDriver(id, Driver)

    def removeDriver(self, driver):
        return DBMS.DriverdatabaseManagement(self.connection).removeDriver(driver)
        
    def takePassanger(self, DriverID, PassangerID):
        return DBMS.PassangersdatabaseManagement(self.connection).updatePassangerTransit(PassangerID, DriverID)
    
    def getPassanger(self, PassangerId):
        return DBMS.PassangersdatabaseManagement(self.connection).getPassanger(PassangerId)

    def getDrivers(self, PassangerId):
        return DBMS.DriverdatabaseManagement(self.connection).getDrivers()