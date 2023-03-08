
from commands.DriverAbstractCommands import DriverCommands


class NoneCommand(DriverCommands):


    def execute(self):
        return super().execute("noCommand")