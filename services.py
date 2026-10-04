from __future__ import annotations

from models import Appointment, DomainError
from storage import JsonStorage


class AppointmentService:
    def __init__(self, storage: JsonStorage) -> None:
        self.storage = storage

    def list(self) -> list[Appointment]:
        return [Appointment.from_dict(item) for item in self.storage.load()["appointments"]]

    def get(self, appointment_id: int) -> Appointment:
        for appointment in self.list():
            if appointment.id == appointment_id:
                return appointment
        raise DomainError("agendamento não encontrado.")

    def create(self, person_name: str, start: str, procedure: str) -> Appointment:
        data = self.storage.load()
        appointment_id = data.get("next_appointment_id", 1)
        appointment = Appointment(person_name, start, procedure, id=appointment_id)
        data["appointments"].append(appointment.to_dict())
        data["next_appointment_id"] = appointment_id + 1
        self.storage.save(data)
        return appointment

    def update(
        self,
        appointment_id: int,
        person_name: str | None = None,
        start: str | None = None,
        procedure: str | None = None,
        room: int | None = None,
    ) -> Appointment:
        current = self.get(appointment_id)
        updated = Appointment(
            person_name or current.person_name,
            start or current.start,
            procedure or current.procedure,
            room if room is not None else current.room,
            current.id,
        )
        self._validate_room(updated.room)
        data = self.storage.load()
        data["appointments"] = [updated.to_dict() if item["id"] == appointment_id else item for item in data["appointments"]]
        self.storage.save(data)
        return updated

    def delete(self, appointment_id: int) -> None:
        self.get(appointment_id)
        data = self.storage.load()
        data["appointments"] = [item for item in data["appointments"] if item["id"] != appointment_id]
        self.storage.save(data)

    def _validate_room(self, room: int | None) -> None:
        if room is None:
            return
        clinic_data = self.storage.load()["clinic"]
        if clinic_data is not None and room > int(clinic_data["max_rooms"]):
            raise DomainError(f"a sala {room} não existe na clínica cadastrada.")
