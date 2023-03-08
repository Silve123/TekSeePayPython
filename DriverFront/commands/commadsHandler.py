from Driver import Driver
from commands.changeStatus import updateStatus
from commands.quitCommand import QuitCommand
from commands.noCommand import NoneCommand
from commands.takePassangerCommand import takePassanger


class commandsHandler:
    def __init__(self, commandString, server, Driver: Driver = None) -> None:
        self.server = server
        self.driver = Driver
        self.commandString = commandString
    
    def createCommand(self):
        commandSplit = self.commandString.split(" ")
        if self.commandString.lower() in ["quit","shut down"]:
            return QuitCommand(self.server)
        if self.commandString.lower() in ["load", "idle", "enroute"]:
            updatecommand = updateStatus(self.server)
            updatecommand.status(self.commandString.lower())
            return updatecommand
        if  commandSplit[0].lower() == "passanger" and len(commandSplit) == 2:
            passangerCommand = takePassanger(self.server)
            passangerCommand.setPassangerID(self.commandString.split(" ")[1])
            return passangerCommand

        return NoneCommand(self.server)