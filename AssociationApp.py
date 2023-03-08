from http import HTTPStatus
from http.client import HTTPConnection
import json


def startApp():
    DriverId = input("Input Association ID: ")
    client = HTTPConnection("localhost","5000")
    client.request("GET", f"/association/{DriverId}")
    response = client.getresponse()
    print(response.status)
    if response.status != HTTPStatus.NOT_FOUND:
        response = brushResponse(response)
        print(response)

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
    responseJson = json.dumps(responseDict)
    return responseJson

if __name__ == "__main__":
    startApp()