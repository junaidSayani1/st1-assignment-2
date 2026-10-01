from domain.models.appointment import Appointment
from repositories.appointment_repository import AppointmentRepository


class InMemoryAppointmentRepository(AppointmentRepository):

    def __init__(self) -> None:
        self._appointments: dict[int, Appointment] = {}

    def save(self, appointment: Appointment) -> None:
        appointment_id = appointment.get_appointment_details()["appointment_id"]
        self._appointments[appointment_id] = appointment

    def find_by_id(self, appointment_id: int) -> Appointment | None:
        return self._appointments.get(appointment_id)

    def find_all(self) -> list[Appointment]:
        return list(self._appointments.values())
