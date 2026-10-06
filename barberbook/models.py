from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class User:
    id: str
    role: str = 'client'

@dataclass(frozen=True)
class Service:
    id: str
    name: str
    minutes: int
    price: int
    active: bool = True

@dataclass
class Appointment:
    id: str
    client_id: str
    barber_id: str
    service_id: str
    start: datetime
    end: datetime
    price: int
    state: str = 'confirmed'
