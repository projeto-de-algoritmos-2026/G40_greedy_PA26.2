"""Modelos e regras básicas do domínio da clínica."""

from __future__ import annotations

from typing import Any

PROCEDURES: dict[str, int] = {
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
    def __init__(self, person_name: str, start: str, procedure: str, room: int | None = None, id: int | None = None) -> None:
        self.id = id
        self.person_name = person_name
        self.start = start
        self.procedure = procedure
        self.room = room

        if self.procedure not in PROCEDURES:
            raise DomainError("procedimento inválido.")

    @property
    def duration_minutes(self) -> int:
        return PROCEDURES[self.procedure]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "person_name": self.person_name,
            "start": self.start,
            "procedure": self.procedure,
            "duration_minutes": self.duration_minutes,
            "room": self.room,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Appointment":
        return cls(data["person_name"], data["start"], data["procedure"], data.get("room"), data.get("id"))
