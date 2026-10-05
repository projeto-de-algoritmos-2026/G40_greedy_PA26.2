"""Modelos e regras básicas do domínio da clínica."""

from __future__ import annotations
from typing import Any
from datetime import datetime

PROCEDURES = {
    "consulta clínica geral": 30,
    "retorno": 15,
    "avaliação clínica": 45,
    "curativo": 30,
    "vacinação": 15,
    "check-up": 60,
}


class DomainError(ValueError):
    pass


class Clinic:
    def __init__(self, name: str, max_rooms: int, doctors: dict[str, str]) -> None:
        self.name = name
        self.max_rooms = max_rooms
        self.doctors = doctors

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "max_rooms": self.max_rooms, "doctors": self.doctors}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Clinic":
        return cls(data["name"], int(data["max_rooms"]), data["doctors"])


class Appointment:
    def __init__(self, person_name, date, start, procedure, room=None, id=None):
        self.id = id
        self.person_name = person_name
        self.date = date
        self.start = start
        self.procedure = procedure
        self.room = room

        if self.procedure not in PROCEDURES:
            raise DomainError("procedimento inválido.")

        self.start_minutes  

    @property
    def duration_minutes(self):
        return PROCEDURES[self.procedure]

    @property
    def start_minutes(self):
        try:
            moment = datetime.strptime(f"{self.date} {self.start}", "%Y-%m-%d %H:%M")
        except ValueError:
            raise DomainError("data ou horário inválido, use AAAA-MM-DD e HH:MM.")
        return moment.toordinal() * 1440 + moment.hour * 60 + moment.minute

    @property
    def end_minutes(self):
        return self.start_minutes + self.duration_minutes

    def to_dict(self):
        return {
            "id": self.id,
            "person_name": self.person_name,
            "date": self.date,
            "start": self.start,
            "procedure": self.procedure,
            "duration_minutes": self.duration_minutes,
            "room": self.room,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["person_name"],
            data["date"],
            data["start"],
            data["procedure"],
            data.get("room"),
            data.get("id"),
        )
