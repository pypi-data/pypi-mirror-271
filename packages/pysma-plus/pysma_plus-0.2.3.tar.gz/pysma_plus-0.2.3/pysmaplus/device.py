from abc import ABC, abstractmethod
from typing import Dict
from .sensor import Sensors

class Device(ABC):

    @abstractmethod
    async def get_sensors(self) -> Sensors:
        pass
    
    @abstractmethod
    async def new_session(self) -> bool:
        pass

    @abstractmethod
    async def device_info(self) -> dict:
        pass

    @abstractmethod
    async def read(self, sensors: Sensors) -> bool:
        pass

    @abstractmethod
    async def close_session(self) -> None:
        pass

    @abstractmethod
    async def get_debug(self) -> Dict:
        pass
