
try:
    from DriverFront.Passanger import Passanger
except ModuleNotFoundError:
    from Passanger import Passanger



class DriverStatus:
    IDLE = 0
    LOADING = 1
    ENROUTE = 2
    NOT_KNOWN = 10

    def getStatus(self, statusString):
        if statusString == "load":
            return DriverStatus.LOADING
        elif statusString == "idle":
            return DriverStatus.IDLE
        elif statusString == "enroute":
            return DriverStatus.ENROUTE
        return DriverStatus.NOT_KNOWN

class Driver:

    def __init__(self, name, surname, numberPlate, seatsNo, status = DriverStatus.IDLE, association = None):
        self.name = name
        self.surname = surname
        self.numberPlate = numberPlate
        self.seatsAvailable = int(seatsNo)
        self.passengers = []
        self.driverStatus = status
        self.Association = association
        self.userName = name[:3]+surname[:3]+numberPlate.replace(" ","")
    
    
    def __str__(self) -> str:
        return f"--> Driver: {self.name} {self.surname} |-| \
Number Plate: '{self.numberPlate}' |-| Avil Seats: {self.seatsAvailable}" 

    
    def getDetails(self):
        return self.name, self.surname, self.numberPlate, self.seatsAvailable, self.driverStatus

    def getSeatsAvailable(self):
        return self.seatsAvailable

    def setAssociation(self, Association):
        self.Association = Association
    
    def getAssociation(self):
        return self.Association
    
    def setDriverStatus(self, driverStatus: DriverStatus):
        self.driverStatus = driverStatus

    def getPassengers(self):
        return self.passengers
    
    def getUserName(self):
        return self.userName

    def takeSeat(self):
        self.seatsAvailable-=1

    def takePassanger(self,passenger):
        if type(passenger) != type(Passanger("","")):
            print("Not a valid Passenger")
            return
        self.takeSeat()
        self.passengers.append(passenger)

