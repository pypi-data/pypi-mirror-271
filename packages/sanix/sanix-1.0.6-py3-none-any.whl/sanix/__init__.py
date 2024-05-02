"""Sanix API class."""
import datetime
import re
from zoneinfo import ZoneInfo
import requests

from .const import (
    ATTR_API_BATTERY,
    ATTR_API_DEVICE_NO,
    ATTR_API_DISTANCE,
    ATTR_API_FILL_PERC,
    ATTR_API_SERVICE_DATE,
    ATTR_API_SSID,
    ATTR_API_STATUS,
    ATTR_API_TIME
)
from .exceptions import SanixException, SanixInvalidAuthException
from .models import Measurement

class Sanix:
    """Sanix API."""
    SANIX_API_HOST = "https://sanix.bitcomplex.pl"

    def __init__(self, serial_no, token) -> None:
        """Initialize the class instance."""
        self._serial_no = serial_no
        self._token = token

    def fetch_data(self):
        """Fetch the update."""
        _url = f"{self.SANIX_API_HOST}/api/measurement/read.php?serial_no={self._serial_no}&auth_token={self._token}"

        try:
            resp = requests.get(_url, timeout=10)
            resp.raise_for_status()
            _json = resp.json()
            return Measurement(
                battery=_json[ATTR_API_BATTERY],
                device_no=_json[ATTR_API_DEVICE_NO],
                distance=_json[ATTR_API_DISTANCE],
                fill_perc=_json[ATTR_API_FILL_PERC],
                service_date=datetime.datetime.strptime(_json[ATTR_API_SERVICE_DATE], "%d.%m.%Y").date() if re.match('\d{2}.\d{2}.\d{4}', _json[ATTR_API_SERVICE_DATE]) else None,
                ssid=_json[ATTR_API_SSID],
                status=_json[ATTR_API_STATUS],
                time=datetime.datetime.strptime(_json[ATTR_API_TIME], "%d.%m.%Y %H:%M:%S").replace(tzinfo=ZoneInfo("Europe/Warsaw"))
            )
        except requests.HTTPError as err:
            if err.response is not None:
                if err.response.status_code == 401:
                    raise SanixInvalidAuthException("Could not authorize.") from err
        except requests.ConnectTimeout as ex:
            raise SanixException("Connection timeout while connecting to Sanix API") from ex
        except requests.ConnectionError as ex:
            raise SanixException("Connection error while connecting to Sanix API") from ex
