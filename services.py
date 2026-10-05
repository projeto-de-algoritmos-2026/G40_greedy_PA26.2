from __future__ import annotations

from models import Appointment, DomainError
from schedule import assign_rooms
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

    def create(self, person_name, date, start, procedure):
        data = self.storage.load()

        if data["clinic"] is None:
            raise DomainError("nenhuma clínica cadastrada.")
        max_rooms = int(data["clinic"]["max_rooms"])

        appointment_id = data.get("next_appointment_id", 1)
        appointment = Appointment(person_name, date, start, procedure, id=appointment_id)

        everything = [Appointment.from_dict(item) for item in data["appointments"]]
        everything.append(appointment)

        rooms_by_id, rooms_needed = assign_rooms(everything)
        if rooms_needed > max_rooms:
            raise DomainError(
                "não há como atender: o horário solicitado exige "
                f"{rooms_needed} salas, mas a clínica possui apenas {max_rooms}."
            )

        for item in everything:
            item.room = rooms_by_id[item.id]

        data["appointments"] = [item.to_dict() for item in everything]
        data["next_appointment_id"] = appointment_id + 1
        self.storage.save(data)
        return appointment

    def update(self, appointment_id, person_name=None, date=None, start=None, procedure=None, room=None):
        current = self.get(appointment_id)
        updated = Appointment(
            person_name or current.person_name,
            date or current.date,
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
