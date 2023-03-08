
from abc import ABC, abstractmethod


class Passanger(ABC):

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
    
    
    def getDetails(self):
        return self.name, self.surname