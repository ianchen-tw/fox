from abc import ABC, abstractmethod


class I_TargetObject(ABC):
    @abstractmethod
    def fetch(self):
        pass

    @abstractmethod
    def parse(self):
        pass