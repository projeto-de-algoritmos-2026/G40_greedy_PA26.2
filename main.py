import json

from models import Clinic, DomainError, PROCEDURES
from services import AppointmentService
from storage import JsonStorage


def clear_screen():
    print("\033[2J\033[H", end="")


def show(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def read_doctors(max_rooms):
    doctors = {}
    for room in range(1, max_rooms + 1):
        doctors[str(room)] = input(f"Médico da sala {room}: ")
    return doctors


def read_procedure(current=None):
    procedures = list(PROCEDURES)
    for number, procedure in enumerate(procedures, 1):
        print(f"{number} - {procedure} ({PROCEDURES[procedure]} minutos)")

    value = input("Número do procedimento: ")
    if not value and current:
        return current

    number = int(value)
    if number < 1 or number > len(procedures):
        raise DomainError("procedimento inválido.")
    return procedures[number - 1]


def main():
    storage = JsonStorage("data.json")
    appointments = AppointmentService(storage)

    while True:
        clear_screen()
        print("\n1 - Criar clínica")
        print("2 - Consultar clínica")
        print("3 - Atualizar clínica")
        print("4 - Excluir clínica")
        print("5 - Criar agendamento")
        print("6 - Listar agendamentos")
        print("7 - Atualizar agendamento")
        print("8 - Excluir agendamento")
        print("0 - Sair")

        option = input("Opção: ")
        clear_screen()

        try:
            if option == "0":
                break

            if option == "1":
                data = storage.load()
                if data["clinic"] is not None:
                    raise DomainError("já existe uma clínica cadastrada.")

                name = input("Nome da clínica: ")
                max_rooms = int(input("Quantidade de salas: "))
                clinic = Clinic(name, max_rooms, read_doctors(max_rooms))
                data["clinic"] = clinic.to_dict()
                storage.save(data)
                show(clinic.to_dict())

            elif option == "2":
                show(storage.load()["clinic"])

            elif option == "3":
                data = storage.load()
                if data["clinic"] is None:
                    raise DomainError("nenhuma clínica cadastrada.")

                clinic = Clinic.from_dict(data["clinic"])
                name = input(f"Nome [{clinic.name}]: ") or clinic.name
                value = input(f"Quantidade de salas [{clinic.max_rooms}]: ")
                max_rooms = int(value) if value else clinic.max_rooms
                clinic = Clinic(name, max_rooms, read_doctors(max_rooms))
                data["clinic"] = clinic.to_dict()
                storage.save(data)
                show(clinic.to_dict())

            elif option == "4":
                data = storage.load()
                if data["clinic"] is None:
                    raise DomainError("nenhuma clínica cadastrada.")
                data["clinic"] = None
                storage.save(data)
                print("Clínica excluída.")

            elif option == "5":
                person_name = input("Nome da pessoa: ")
                start = input("Horário (HH:MM): ")
                procedure = read_procedure()
                appointment = appointments.create(
                    person_name,
                    start,
                    procedure,
                )
                show(appointment.to_dict())

            elif option == "6":
                show([item.to_dict() for item in appointments.list()])

            elif option == "7":
                appointment_id = int(input("ID do agendamento: "))
                appointment = appointments.get(appointment_id)
                person = input(f"Nome [{appointment.person_name}]: ") or appointment.person_name
                start = input(f"Horário [{appointment.start}]: ") or appointment.start
                print(f"Procedimento atual: {appointment.procedure}")
                procedure = read_procedure(appointment.procedure)
                room = input("Sala (vazio mantém a atual): ")
                changes = {"person_name": person, "start": start, "procedure": procedure}
                if room:
                    changes["room"] = int(room)
                show(appointments.update(appointment_id, **changes).to_dict())

            elif option == "8":
                appointments.delete(int(input("ID do agendamento: ")))
                print("Agendamento excluído.")

            else:
                print("Opção inválida.")

        except (DomainError, ValueError, json.JSONDecodeError) as error:
            print(f"Erro: {error}")

        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()
