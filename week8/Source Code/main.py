from persistence.in_memory_appointment_repository import InMemoryAppointmentRepository
from presentation.view import demo
from services.appointment_service import AppointmentService


if __name__ == "__main__":
    demo(AppointmentService(InMemoryAppointmentRepository()))
