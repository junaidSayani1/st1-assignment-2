from datetime import datetime
from enum import Enum

class Patient:
    pass

class Appointment:
    pass

class Practitioner:
    pass


class AppointmentStatus(Enum):
    BOOKED = "BOOKED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Practitioner:

    def __init__(self, practitioner_id: int, name: str, speciality: str) -> None:
        self._id = practitioner_id
        self._name = name
        self._speciality = speciality

    def get_practitioner_details(self) -> Practitioner:
        pass

    def set_practitioner_details(self, name: str | None, speciality: str | None) -> None:
        pass


class Patient:

    def __init__(self, patient_id: int, name: str, date_of_birth: datetime, medical_history: list[str] | None = None) -> None:
        self._id = patient_id
        self._name = name
        self._date_of_birth = date_of_birth
        if medical_history is None:
            self._medical_history = []
        else:
            self._medical_history = medical_history

    def get_patient_details(self) -> Patient:
        pass

    def update_patient_details(self, name: str | None, date_of_birth: datetime | None, medical_history: list[str] | None) -> None:
        pass

    def get_medical_history(self) -> list[str]:
        pass

    def validate_details(self, validation_Patient: Patient) -> None:
        pass



class Appointment:

    def __init__(self, appointment_id: int | None, patient_id: int | None, practitioner_id: int | None, time_slot: datetime | None, status: AppointmentStatus = AppointmentStatus.BOOKED):
        self._id = appointment_id
        self._patient_id = patient_id
        self._practitioner_id = practitioner_id
        self._time_slot = time_slot
        self._status = status

    def get_appointment_details(self) -> Appointment:
        pass

    def book_appointment(self, appointment_id: int, patient_id: int, practitioner_id: int, time_slot: datetime) -> None:
        pass

    def cancel_appointment(self) -> None:
        pass

    def update_appointment(self, patient_id: int | None, practitioner_id: int | None, time_slot: datetime | None, status: AppointmentStatus | None) -> None:
        pass

