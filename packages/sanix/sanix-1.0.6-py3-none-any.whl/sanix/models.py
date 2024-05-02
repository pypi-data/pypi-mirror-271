from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class Measurement:
    battery: int
    device_no: str
    distance: int
    fill_perc: int
    service_date: date
    ssid: str
    status: str
    time: datetime

