from abc import ABC, abstractmethod


class DoubleWell(ABC):

    @abstractmethod
    def __call__(self, pf): ...

    @abstractmethod
    def prime(self, pf): ...

    @abstractmethod
    def c(self, pf): ...

    @abstractmethod
    def e(self, pf): ...

    @abstractmethod
    def cprime(self, pf): ...

    @abstractmethod
    def eprime(self, pf): ...
