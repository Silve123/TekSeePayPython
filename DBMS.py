import sqlite3

from DriverFront.Driver import Driver, DriverStatus
from DriverFront.Passanger import Passanger

class AssociationsdatabaseManagement:
    """"""

    def __init__(self,connection):
        self.dbConnection = connection


    def dropTable(self):
        # Drops the Associations table 
        try:
            self.dbConnection.execute(f"DROP TABLE IF EXISTS Associations")
            return True
        except sqlite3.OperationalError as e:
            print(e)
            return None
    

    def createTable(self):
        # Creates the Associations table 
        try:
            self.dropTable()
            self.dbConnection.execute("CREATE TABLE Associations( \
associations_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
name TEXT NOT NULL, abriv TEXT NOT NULL, association_no TEXT NOT NULL)")
            return True
        except sqlite3.OperationalError as e:
            print(e)
            return None
            
    
    def insertIntoTable(self, AssociationObj):
        # Inserts into the Associations table 
        try:
            self.dbConnection.execute("INSERT INTO Associations (name,abriv,association_no)"+
                                f"VALUES ('{AssociationObj.getName()}','{AssociationObj.getAbriviation()}','{AssociationObj.getAssociationNo()}' )")
            self.dbConnection.commit()
            # Inserting Each Driver into the Driver Table
            for Driver in AssociationObj.getDrivers():
                self.insertIntoDriversTable(Driver, AssociationObj.getAssociationNo())
            return True
        except sqlite3.OperationalError as e:
            print(e)
            return None
    

    def insertIntoDriversTable(self, Driver, ass_no):
        try:
            driverDetails = Driver.getDetails()
            self.dbConnection.execute("INSERT INTO Drivers (driver_id,name,surname,no_plate,seat_no,association_no, status)"+
                                f"VALUES ('{Driver.getUserName()}','{driverDetails[0]}','{driverDetails[1]}',"+
                                f"'{driverDetails[2]}','{driverDetails[3]}','{ass_no}', '{driverDetails[4]}')")
            self.dbConnection.commit()
            print(f"Inserted {driverDetails[0]} {driverDetails[1]} into Drivers Table")
        except sqlite3.OperationalError as e:
            print(e)
            return None

    def getAssociation(self, id):
        try:
            # sqlite3.Connection.
            passOne = self.dbConnection.execute(f"SELECT * FROM Associations WHERE association_no LIKE '%{id}%'").fetchone()
            return passOne
            
        except sqlite3.OperationalError as e:
            print(e)
            return None

    def closeConnection(self):
        # Closes the given connection 
        self.dbConnection.close()





class DriverdatabaseManagement:
    """"""


    def __init__(self,connection):
        self.dbConnection = connection


    def dropTable(self):
        # Drops the Associations table 
        try:
            self.dbConnection.execute(f"DROP TABLE IF EXISTS Drivers")
            return True
        except sqlite3.OperationalError as e:
            print(e)
            return None
    

    def createTable(self):
        # Creates the Associations table 
        try:
            self.dropTable()
            self.dbConnection.execute("CREATE TABLE Drivers( \
driver_id TEXT NOT NULL PRIMARY KEY, \
name TEXT NOT NULL, surname TEXT NOT NULL, no_plate TEXT NOT NULL,seat_no INTEGER NOT NULL,status INTEGER NOT NULL, association_no TEXT NOT NULL,\
FOREIGN KEY (association_no) REFERENCES Associations)")
            return True
        except sqlite3.OperationalError as e:
            print(e)
            return None
    

    def closeConnection(self):
        # Closes the given connection 
        self.dbConnection.close()

    def getDriver(self, id):
        try:
            # sqlite3.Connection.
            passOne = self.dbConnection.execute(f"SELECT * FROM Drivers WHERE driver_id LIKE '%{id}%'").fetchone()
            if(passOne[0] == id):
                return passOne
            return None
            
        except sqlite3.OperationalError as e:
            print(e)
            return None

    def getDrivers(self):
        try:
            # sqlite3.Connection.
            passOne = self.dbConnection.execute(f"SELECT no_plate, seat_no, status FROM Drivers ").fetchall()
            return passOne
            
        except sqlite3.OperationalError as e:
            print(e)
            return None
    
    def updateDriverStatus(self, id, status):
        try:
            passOne = self.dbConnection.execute(f"SELECT * FROM Drivers WHERE driver_id LIKE '%{id}%'").fetchone()
            passObj = Driver(passOne[1], passOne[2], passOne[3], passOne[4], passOne[5], passOne[6])
            passObj.setDriverStatus(DriverStatus().getStatus(status))
            self.dbConnection.execute(f"DELETE FROM Drivers WHERE driver_id IN ('{id}')")
            self.dbConnection.commit()
            self.dbConnection.execute(self.driverUpdateSqlString(passObj))
            self.dbConnection.commit()
            return passObj

        except sqlite3.OperationalError as e:
            print(e)
            return None

    def removeDriver(self, driver):
        try:
            self.dbConnection.execute(f"DELETE FROM Drivers WHERE driver_id IN ('{driver.getUserName()}')")
            self.dbConnection.commit()
        except sqlite3.OperationalError as e:
            print(e)

    def updateDriver(self, id, Driver):
        try:
            passOne = self.dbConnection.execute(f"SELECT * FROM Drivers WHERE driver_id LIKE '%{id}%'").fetchone()
            self.dbConnection.execute(f"DELETE FROM Drivers WHERE driver_id IN ('{id}')")
            self.dbConnection.commit()
            self.dbConnection.execute(self.driverUpdateSqlString(Driver))
            self.dbConnection.commit()
            return Driver

        except sqlite3.OperationalError as e:
            print(e)
            return None
    
    def driverUpdateSqlString(self, passObj: Driver):
        return f"INSERT INTO Drivers (driver_id,name,surname,no_plate,seat_no,association_no, status)\
                                VALUES ('{passObj.getUserName()}',\
                                '{passObj.getDetails()[0]}',\
                                '{passObj.getDetails()[1]}',\
                                '{passObj.getDetails()[2]}',\
                                '{passObj.getDetails()[3]}',\
                                '{passObj.getAssociation()}',\
                                '{passObj.getDetails()[4]}')"
    


"""Passanger Database Management"""
class PassangersdatabaseManagement:
    """"""


    def __init__(self,connection):
        self.dbConnection = connection


    def dropTable(self):
        # Drops the Associations table 
        try:
            self.dbConnection.execute(f"DROP TABLE IF EXISTS Passangers")
            return True
        except sqlite3.OperationalError as e:
            print(e)
            return None
    

    def createTable(self):
        # Creates the Associations table 
        try:
            self.dropTable()
            self.dbConnection.execute("CREATE TABLE Passangers ( \
passanger_id TEXT NOT NULL PRIMARY KEY, \
name TEXT NOT NULL, surname TEXT NOT NULL, driver_id TEXT NOT NULL,\
FOREIGN KEY (driver_id) REFERENCES Drivers)")
            return True
        except sqlite3.OperationalError as e:
            print(e)
            return None
    

    def closeConnection(self):
        # Closes the given connection 
        self.dbConnection.close()

    
    def insertPassanger(self, PassangerObj):
          # Inserts into the Associations table 
        try:
            self.dbConnection.execute(self.passangerUpdateSqlString(PassangerObj))
            self.dbConnection.commit()
            return True
        except sqlite3.OperationalError as e:
            print(e)
            return None
    
    def updatePassangerTransit(self, id, driverId):
        try:
            passOne = self.dbConnection.execute(f"SELECT * FROM Passangers WHERE passanger_id LIKE '%{id}%'").fetchone()
            passObj = Passanger(passOne[1],passOne[2], passOne[0])
            passObj.setDriver(driverId)
            self.dbConnection.execute(f"DELETE FROM Passangers WHERE passanger_id IN ('{id}')")
            self.dbConnection.commit()
            self.insertPassanger(passObj)
            self.dbConnection.commit()
            return passObj

        except sqlite3.OperationalError as e:
            print(e)
            return None
    
    def passangerUpdateSqlString(self, PassangerObj: Passanger):
        passangerString = f"""INSERT INTO Passangers (passanger_id,name,surname,driver_id)
                VALUES ('{PassangerObj.getDetails()[0]}','{PassangerObj.getDetails()[1]}',
                '{PassangerObj.getDetails()[2]}','{PassangerObj.getDetails()[3]}')"""
        return passangerString

    def getPassanger(self, id):
        try:
            # sqlite3.Connection.
            passOne = self.dbConnection.execute(f"SELECT * FROM Passangers WHERE passanger_id LIKE '%{id}%'").fetchone()
            if passOne != None and passOne[0] == id:
                return passOne
            return None
            
        except sqlite3.OperationalError as e:
            print(e)
            return None
