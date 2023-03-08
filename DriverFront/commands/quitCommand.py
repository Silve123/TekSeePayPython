
from commands.DriverAbstractCommands import DriverCommands


class QuitCommand(DriverCommands):
    
    def execute(self):
        return super().execute("quit")