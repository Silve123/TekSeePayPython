
from os import stat
from UI.AbstractUI import AbstractUserInterface


class TerminalView(AbstractUserInterface):
    
    def greet(self):
        name = self.driverDict["name"]
        print(f"Hello {name}")
        self.displayBanner()
        return super().greet()

    def displayBanner(self):
        name = self.driverDict["name"]
        surname = self.driverDict["surname"]
        associationNo = self.driverDict["associationNo"]
        numberPlate = self.driverDict["numberPlate"]
        status = self.driverDict["status"]
        seatsAvail = self.driverDict["seatsAvailable"]

        banner = f"""{"-"*50}\nName: {name.upper()}\nSurname: {surname.upper()}
Association: {associationNo.upper()}\nSeats: {seatsAvail}\nReg: {numberPlate.upper()}
Status: {status}\n
{"-"*50}"""
        print(banner)
        
        return super().displayBanner()