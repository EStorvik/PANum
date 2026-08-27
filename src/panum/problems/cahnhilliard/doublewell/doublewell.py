from abc import ABC, abstractmethod

class DoubleWell(ABC):


    @abstractmethod
    def __call__(self, pf):
        ...

    @abstractmethod
    def prime(self, pf):
        ...