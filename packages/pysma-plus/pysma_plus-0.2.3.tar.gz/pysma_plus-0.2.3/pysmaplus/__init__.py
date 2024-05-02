"""SMA WebConnect library for Python.

See: http://www.sma.de/en/products/monitoring-control/webconnect.html

Source: http://www.github.com/kellerza/pysma
"""
import logging
from typing import Optional

from aiohttp import ClientSession
from .device_webconnect import SMAwebconnect
from .device_ennexos import SMAennexos
from .device_speedwire import SMAspeedwireINV
from .device_em import SMAspeedwireEM
from .device import Device
_LOGGER = logging.getLogger(__name__)


# Backward compatibility
def SMA(session, url, password, group):
    return SMAwebconnect(session, url, password=password, group=group)


def getDevice(session: ClientSession,
        url: str,
        password: Optional[str] = None,
        groupuser: str = "user",
        accessmethod: str = "webconnect"
    ) -> Device:
        _LOGGER.debug(f"Device Called! Url: {url} User/Group: {groupuser} Accessmethod: {accessmethod}")
        if (accessmethod == "webconnect"):
            return SMAwebconnect(session, url, password=password, group=groupuser)
        elif (accessmethod == "ennexos"):
            return SMAennexos(session, url, password=password, group=groupuser)
        elif (accessmethod == "speedwire") or (accessmethod == "speedwireem"):
              return SMAspeedwireEM()
        elif (accessmethod == "speedwireinv"):
              return SMAspeedwireINV(host = url, password= password, group=groupuser)
        else:
             return None
