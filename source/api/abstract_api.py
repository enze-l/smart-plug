from .utils.abc import ABC, abstractmethod


class AbstractAPI(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
