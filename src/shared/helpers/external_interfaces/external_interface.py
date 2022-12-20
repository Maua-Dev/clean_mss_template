from abc import ABC, abstractmethod


class IRequest(ABC):

    @property
    def data(self) -> dict:
        pass


class IResponse(ABC):

    @property
    @abstractmethod
    def status_code(self) -> int:
        pass

    @property
    @abstractmethod
    def data(self) -> dict:
        pass
