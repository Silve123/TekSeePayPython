from http.client import HTTPConnection
import sys
from UI.Terminal import TerminalView
from commands.commadsHandler import commandsHandler

class DriverApp:

    def __init__(self, ID=None) -> None:
        self.Alive = False
        self.ID = ID

    def startApp(self):
        if self.ID == None:
             self.ID = input("Input Driver ID: ")
        self.server = HTTPConnection("localhost","6666")
        print("Getting Details...")
        driverDict = commandsHandler("", self).createCommand().getDetails()
        display = TerminalView(driverDict)
        display.greet()
        self.Alive = True
        while self.Alive:
            command = commandsHandler(input("Command: "), self).createCommand()
            command.execute()
            if command.getName() == "quit":
                self.Alive = False
            elif command.getName() == "noCommand":
                print("Unsupported Command")
      


if __name__ == "__main__":
    if len(sys.argv) < 2:
        DriverApp().startApp()
    else:
        DriverApp(sys.argv[1]).startApp()