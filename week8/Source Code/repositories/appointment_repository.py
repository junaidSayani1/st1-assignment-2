from abc import ABC, abstractmethod

from domain.models.appointment import Appointment


class AppointmentRepository(ABC):

    @abstractmethod
    def save(self, appointment: Appointment) -> None:
        pass

    @abstractmethod
    def find_by_id(self, appointment_id: int) -> Appointment | None:
        pass

    @abstractmethod
    def find_all(self) -> list[Appointment]:
        pass
