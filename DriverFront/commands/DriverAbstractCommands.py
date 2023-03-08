from abc import ABC, abstractmethod
from http import HTTPStatus
from http.client import HTTPConnection
from Driver import Driver


class DriverCommands(ABC):
    
    def __init__(self, server, Driver: Driver = None, ) -> None:
        self.Driver = Driver
        self.name = None
        self.server = server
        super().__init__()
    
    def getName(self):
        return self.name

    
    def brushResponse(response):
        response = response.read().__str__().replace("\\n","")
        response = response.replace(" ","")
        response = response.replace("\"","")
        response = response[3:-2].split(",")
        response = [item.split(":") for item in response]
        responseDict = {}
        for item in response:
            try:
                responseDict[item[0]] = int(item[1])
            except ValueError:
                responseDict[item[0]] = item[1]
        
        return responseDict
    
    def getDetails(self):
        self.server.server.request("GET", f"/driver/{self.server.ID}")
        response = self.server.server.getresponse()
        if response.status != HTTPStatus.NOT_FOUND:
            response = DriverCommands.brushResponse(response)
            return response
        else:
            return response
    
    @abstractmethod
    def execute(self, name):
        self.name = name

    

