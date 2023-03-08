
from abc import ABC, abstractmethod


class AbstractUserInterface(ABC):
    def __init__(self, driverDict) -> None:
        self.driverDict = driverDict
        super().__init__()

    @abstractmethod
    def greet(self):
        pass

    @abstractmethod
    def displayBanner(self):
        pass