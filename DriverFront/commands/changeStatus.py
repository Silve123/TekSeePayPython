from UI.Terminal import TerminalView
from commands.DriverAbstractCommands import DriverCommands


class updateStatus(DriverCommands):

    def execute(self):
        self.updateStatus()
        driverDict = self.getDetails()
        display = TerminalView(driverDict)
        display.displayBanner()
        return super().execute("update")
    
    def updateStatus(self):
        self.server.server.request("POST", f"/driver/{self.server.ID}/status", headers = {"status":f"{self.statusType}"})
        response = self.server.server.getresponse()

    def status(self, status):
        self.statusType = status
