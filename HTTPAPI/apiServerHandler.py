from http import HTTPStatus
import json
from Association import Association
from DBMS import AssociationsdatabaseManagement
from DriverFront.Driver import Driver
from DriverFront.Passanger import Passanger

from HTTPAPI.httpAPI import HTTPAPI


class handleGETServerRequest:
    
    def checkPath(requestPath):
        if requestPath.__contains__("/driver/") and requestPath.split("/")[-1].isalnum()\
            and len(requestPath[1:].split("/")) == 2:
            return handlerStatus.DRIVER_ID
        elif requestPath.__contains__("/association/") and requestPath.split("/")[-1].isalnum()\
            and len(requestPath[1:].split("/")) == 2:
            return handlerStatus.ASSOCIATION_ID
        elif requestPath.__contains__("/passanger/") and requestPath.split("/")[-1].isalnum()\
            and requestPath.__contains__("/driversInfo") == False :
            return handlerStatus.PASSANGER_ID
        elif requestPath.__contains__("/passanger/") and requestPath.split("/")[-1].isalnum()\
            and requestPath.__contains__("/driversInfo/") :
            print("perfect")
            return handlerStatus.DRIVERS_FOR_PASSANGER
        else:
            return handlerStatus.NOT_FOUND
    
class handlePOSTServerRequest:
    
    def checkPath(requestPath, data):
            # updating driver status checks
            data = data.split(": ")[-1]
            DriverStatusUpdate = requestPath.__contains__("/driver/") and \
            requestPath.__contains__("/status") and requestPath.split("/")[1].isalnum() \
            and data in ["load", "idle", "enroute"]
            
            # taking passanger checks
            takePassanger = requestPath.__contains__("/driver/") and \
            requestPath.__contains__("/takePassanger") and requestPath.split("/")[1].isalnum()
            if DriverStatusUpdate:
                HTTPAPI().updateDriverStatus(requestPath.split("/")[2], data)
                return handlerStatus.DRIVER_STATUS_UPDATE
            if takePassanger:
                driverId = requestPath.split("/")[2]
                driveRe = HTTPAPI().getDriver(driverId)
                driverHold = Driver(driveRe[1], driveRe[2], driveRe[3], driveRe[4], driveRe[5], driveRe[6])
                driverHold.takeSeat()
                if driverHold.getDetails()[-1] != 1:
                    driverHold.setDriverStatus(1)
                HTTPAPI().removeDriver(driverHold)
                HTTPAPI().updateDriver(driverHold)
                HTTPAPI().takePassanger(requestPath.split("/")[2], data)
                return handlerStatus.DRIVER_TAKE_PASSANGER
                
            
# -----------------------------------------------------------------------------------
#                               helps handleJson to Nevigate Paths
class handlerStatus:
    DRIVERS_FOR_PASSANGER = 6
    DRIVER_ID = 2
    DRIVER_STATUS_UPDATE = 5
    DRIVER_TAKE_PASSANGER = 4
    ASSOCIATION_ID = 1
    PASSANGER_ID = 3
    NOT_FOUND = 100
    


class handleJson:
    def __init__(self, handlerStatus, path, id) -> None:
        self.handlerStatus = handlerStatus
        self.path = path
        self.id = id

    def getDriverJson(self):
        driverTuple = HTTPAPI().getDriver(self.id)
        return json.dumps(
                {   
                    "id": driverTuple[0],
                    "name":driverTuple[1],
                    "surname":driverTuple[2],
                    "numberPlate":driverTuple[3],
                    "seatsAvailable":int(driverTuple[4]),
                    "status":int(driverTuple[5]),
                    "associationNo": driverTuple[6]

                },
                sort_keys=True, indent=4) if driverTuple != None else handlerStatus.NOT_FOUND
    
    def getAssociationJson(self):
        associationTuple = HTTPAPI().getAssociation(self.path.split("/")[-1])
        return json.dumps(
                {   
                    "id": associationTuple[0],
                    "name":associationTuple[1],
                    "abriv":associationTuple[2],
                    "associationNo":associationTuple[3],
                },
                sort_keys=True, indent=4) if associationTuple != None else handlerStatus.NOT_FOUND


    def getPassangerJson(self):
        passangerTuple = HTTPAPI().getPassanger(self.path.split("/")[-1])
        return json.dumps(
                {   
                    "id": passangerTuple[0],
                    "name":passangerTuple[1],
                    "surname":passangerTuple[2],
                    "driver_id":passangerTuple[3],
                },
                sort_keys=True, indent=4) if passangerTuple != None else handlerStatus.NOT_FOUND


    def getDriversJson(self):
        driverList = HTTPAPI().getDrivers(self.id)
        driverJsonList = []
        count = 0
        for driverTuple in driverList:
            count=count+1
            driverJson = json.dumps(
                {   
                    "numberPlate":driverTuple[0],
                    "seatsAvailable":int(driverTuple[1]),
                    "status":int(driverTuple[2]),


                },
                sort_keys=True, indent=4)

            driverJsonList.append(driverJson)
        driversJson = json.dumps({"Drivers":driverJsonList},sort_keys=True, indent=4)
        return driversJson  if driverTuple != None else handlerStatus.NOT_FOUND

    def getJson(self):
        if self.handlerStatus == handlerStatus.DRIVER_ID:
            print("Processing Driver with ID...")
            return self.getDriverJson()
        elif self.handlerStatus == handlerStatus.ASSOCIATION_ID:
            print("Processing Association with ID...")
            return self.getAssociationJson()
        elif self.handlerStatus == handlerStatus.PASSANGER_ID:
            print("Processing Passanger with ID...")
            return self.getPassangerJson()
        elif self.handlerStatus == handlerStatus.DRIVER_STATUS_UPDATE:
            print("Updating Driver Status..")
            return self.getDriverJson()
        elif self.handlerStatus == handlerStatus.DRIVER_TAKE_PASSANGER:
            print("Taking a Passanger...")
            return self.getDriverJson()
        elif self.handlerStatus == handlerStatus.DRIVERS_FOR_PASSANGER:
            print("Processing Drivers for a passanger")
            return self.getDriversJson()
    
