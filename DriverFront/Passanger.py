
from abc import ABC
from datetime import datetime
from http import HTTPStatus
from http.client import HTTPConnection
import json


class Passanger(ABC):

    def __init__(self, name, surname, id=None):
        self.name = name
        self.surname = surname
        self.driver_id = None
        self.id = self.generate_id() if id == None else id

    
    def getDetails(self):
        return self.id, self.name, self.surname, self.driver_id

    def generate_id(self):
        return self.name[-2:]+self.surname[:3]+datetime.now().date().__str__().replace("-","")

    def setDriver(self, driverId):
        self.driver_id = driverId

    def addAuthentication(self, password) -> bool:
        passangerRequest = HTTPConnection("127.0.0.1", 6666)

        data = [[self.id, password, 3]]

        data = json.dumps(data)

        passangerRequest.request("POST", f"/add$Authentication", \
        headers={"data": data})
        requestResponse = passangerRequest.getresponse() 
        print(requestResponse.headers["response"])
        if requestResponse.status != HTTPStatus.CREATED:
            return False
        return True