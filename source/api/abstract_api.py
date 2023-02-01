from .utils.abc import ABC, abstractmethod


class AbstractAPI(ABC):
    @abstractmethod
    def __init__(self, hardware):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def get_html_options(self):
        pass
