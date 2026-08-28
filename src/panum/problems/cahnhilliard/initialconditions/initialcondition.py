from abc import ABC, abstractmethod


class InitialConditionCahnHilliard(ABC):

    @abstractmethod
    def __call__(self, x): ...
