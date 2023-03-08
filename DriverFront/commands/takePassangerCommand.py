from UI.Terminal import TerminalView
from commands.DriverAbstractCommands import DriverCommands



class takePassanger(DriverCommands):

    def execute(self):
        self.addPassanger()
        driverDict = self.getDetails()
        display = TerminalView(driverDict)
        display.displayBanner()
        return super().execute("takePassanger")

    def addPassanger(self):
        self.server.server.request("POST", f"/driver/{self.server.ID}/takePassanger",  headers = {"passangerID":self.passangerID})
        response = self.server.server.getresponse()
        print(response.status)

    def setPassangerID(self, passangerID):
        self.passangerID = passangerID