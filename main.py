from http.server import HTTPServer
import sqlite3
from Association import Association
from DBMS import AssociationsdatabaseManagement, DriverdatabaseManagement, PassangersdatabaseManagement
from DriverFront.Driver import Driver
from DriverFront.Passanger import Passanger
from HTTPAPI.httpServer import MyBaseRequestHandler

def startApp():
    seedData()
    startServer()


def startServer():
    IP, PORT = "127.0.0.1",5555
    server = HTTPServer((IP,PORT),MyBaseRequestHandler)
    print(f"Running on: {IP}:{PORT}")
    print("Starting new client connection...")
    server.serve_forever()

def seedData():
    sqlConnection = sqlite3.connect("testdatabase.db")
    associations = AssociationsdatabaseManagement(sqlConnection)
    drivers = DriverdatabaseManagement(sqlConnection)
    passangers = PassangersdatabaseManagement(sqlConnection)

    associations.createTable()
    drivers.createTable()
    passangers.createTable()

    dummyAss = Association("Orange Farm United Taxi Association", "OFUTA")
    dummyAss.generateAssociationNo()
    dummyAss.addDriver(Driver("Thokozani","Mofokeng","TMK 672 GP", 16))
    dummyAss.addDriver(Driver("Nkomani","Zwide","KLK 521 GP", 22))
    dummyAss.addDriver(Driver("Joseph","Malemela","LPO 721 GP", 16))
    print(dummyAss.addAuthentications("OFUTA123456789@"))

    associations.insertIntoTable(dummyAss)

    # -----------------
    dummyAssTwo = Association("I DOnt know what it means but its popular", "FARADAE")
    dummyAssTwo.generateAssociationNo()
    dummyAssTwo.addDriver(Driver("Nkanyiso","Zulu","OPL 969 GP", 16))
    dummyAssTwo.addDriver(Driver("Loliwe","Lamola","UIO 564 GP", 22))
    print(dummyAssTwo.addAuthentications("FARADAE123456789@"))

    associations.insertIntoTable(dummyAssTwo)

    dummyPass = Passanger("John", "Doe")
    print(dummyPass.addAuthentication("notThisAgain@"))
    passangers.insertPassanger(dummyPass)


if __name__ == "__main__":
    startApp() 
