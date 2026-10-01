from datetime import datetime
from domain.models.enums import AppointmentStatus

from domain.models.exceptions import InvalidIdError, InvalidStatusTransitionError


class Appointment:

    def __init__(self, appointment_id: int, patient_id: int, practitioner_id: int,
                 time_slot: datetime, status: AppointmentStatus = AppointmentStatus.SCHEDULED) -> None:
        self.validate_details(appointment_id, patient_id, practitioner_id)
        self._id = appointment_id
        self._patient_id = patient_id
        self._practitioner_id = practitioner_id
        self._time_slot = time_slot
        self._status = status

    def validate_details(self, appointment_id: int, patient_id: int, practitioner_id: int) -> None:
        if appointment_id <= 0:
            raise InvalidIdError("appointment_id", appointment_id)
        if patient_id <= 0:
            raise InvalidIdError("patient_id", patient_id)
        if practitioner_id <= 0:
            raise InvalidIdError("practitioner_id", practitioner_id)

    def get_appointment_details(self) -> dict:
        return {
            "appointment_id": self._id,
            "patient_id": self._patient_id,
            "practitioner_id": self._practitioner_id,
            "time_slot": self._time_slot,
            "status": self._status.value
        }

    def cancel_appointment(self) -> None:
        
        if self._status == AppointmentStatus.COMPLETED:
            raise InvalidStatusTransitionError("cancel", self._status.value)
        if self._status == AppointmentStatus.CANCELLED:
            raise InvalidStatusTransitionError("cancel", self._status.value)
        self._status = AppointmentStatus.CANCELLED

    def complete_appointment(self) -> None:
        if self._status == AppointmentStatus.CANCELLED:
            raise InvalidStatusTransitionError("complete", self._status.value)
        if self._status == AppointmentStatus.COMPLETED:
            raise InvalidStatusTransitionError("complete", self._status.value)
        self._status = AppointmentStatus.COMPLETED

    def update_appointment(self, patient_id: int | None = None,
                          practitioner_id: int | None = None,
                          time_slot: datetime | None = None) -> None:
        
        if self._status != AppointmentStatus.SCHEDULED:
            raise InvalidStatusTransitionError("update", self._status.value)
        if patient_id is None:
            patient_id = self._patient_id
        if practitioner_id is None:
            practitioner_id = self._practitioner_id
        if time_slot is None:
            time_slot = self._time_slot
        self.validate_details(self._id, patient_id, practitioner_id)
        self._patient_id = patient_id
        self._practitioner_id = practitioner_id
        self._time_slot = time_slot

    def get_status(self) -> AppointmentStatus:
        return self._status
