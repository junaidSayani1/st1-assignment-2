from enum import Enum
from datetime import datetime
from typing import Optional


class AppointmentStatus(Enum):
    """Represents the valid states of an Appointment."""
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Appointment:
    """
    Appointment class represents a healthcare appointment.
    
    Invariants:
    1. appointment_id must be positive integer
    2. patient_id must be positive integer
    3. practitioner_id must be positive integer
    4. time_slot must be in the future
    5. Cancelled appointments remain as objects (status = CANCELLED)
    6. Status transitions are protected (only valid transitions allowed)
    
    Valid State Transitions:
    - SCHEDULED → COMPLETED (appointment occurs)
    - SCHEDULED → CANCELLED (appointment cancelled)
    - COMPLETED → (terminal state, no transitions)
    - CANCELLED → (terminal state, no transitions)
    """

    def __init__(self, appointment_id: int, patient_id: int, practitioner_id: int, 
                 time_slot: datetime, status: AppointmentStatus = AppointmentStatus.SCHEDULED) -> None:
        """
        Initialize an Appointment object with validation.
        
        Args:
            appointment_id: Unique appointment identifier (must be positive)
            patient_id: Patient identifier (must be positive)
            practitioner_id: Practitioner identifier (must be positive)
            time_slot: Appointment date/time (must be in future)
            status: Current appointment status (default: SCHEDULED)
        """
        self.validate_details(appointment_id, patient_id, practitioner_id, time_slot)
        
        self._id = appointment_id
        self._patient_id = patient_id
        self._practitioner_id = practitioner_id
        self._time_slot = time_slot
        self._status = status

    def validate_details(self, appointment_id: int, patient_id: int, 
                        practitioner_id: int, time_slot: datetime) -> None:
        """
        Validates all Appointment invariants.
        
        Invariants checked:
        1. appointment_id must be positive integer
        2. patient_id must be positive integer
        3. practitioner_id must be positive integer
        4. time_slot must be in the future
        
        Raises:
            ValueError: If any invariant is violated
        """
        if appointment_id <= 0:
            raise ValueError(f"Invalid appointment_id: {appointment_id}. Must be positive integer.")
        
        if patient_id <= 0:
            raise ValueError(f"Invalid patient_id: {patient_id}. Must be positive integer.")
        
        if practitioner_id <= 0:
            raise ValueError(f"Invalid practitioner_id: {practitioner_id}. Must be positive integer.")
        
        if time_slot <= datetime.now():
            raise ValueError(f"Invalid time_slot: {time_slot}. Must be in the future.")

    def get_appointment_details(self) -> dict:
        """
        Returns appointment details as a dictionary (safe encapsulation).
        
        Decision: Returns dict instead of self to protect internal state.
        """
        return {
            "appointment_id": self._id,
            "patient_id": self._patient_id,
            "practitioner_id": self._practitioner_id,
            "time_slot": self._time_slot,
            "status": self._status.value
        }

    def cancel_appointment(self) -> None:
        """
        Cancel the appointment.
        
        Decision: Only SCHEDULED appointments can be cancelled.
        COMPLETED and CANCELLED are terminal states.
        
        Raises:
            ValueError: If appointment cannot be cancelled from current state
        """
        if self._status == AppointmentStatus.COMPLETED:
            raise ValueError("Cannot cancel a COMPLETED appointment.")
        
        if self._status == AppointmentStatus.CANCELLED:
            raise ValueError("Appointment is already CANCELLED.")
        
        # SCHEDULED → CANCELLED (valid transition)
        self._status = AppointmentStatus.CANCELLED

    def complete_appointment(self) -> None:
        """
        Mark the appointment as completed.
        
        Decision: Only SCHEDULED appointments can be completed.
        This method is added because completion is a valid
        state transition that should be protected like cancellation.
        
        Raises:
            ValueError: If appointment cannot be completed from current state
        """
        if self._status == AppointmentStatus.CANCELLED:
            raise ValueError("Cannot complete a CANCELLED appointment.")
        
        if self._status == AppointmentStatus.COMPLETED:
            raise ValueError("Appointment is already COMPLETED.")
        
        # SCHEDULED → COMPLETED (valid transition)
        self._status = AppointmentStatus.COMPLETED

    def update_appointment(self, patient_id: int | None = None, 
                          practitioner_id: int | None = None, 
                          time_slot: datetime | None = None) -> None:
        """
        Update appointment details with validation.
        
        Decision: Only SCHEDULED appointments can be updated.
        COMPLETED and CANCELLED appointments cannot be modified.
        Status is NOT updated through this method (use cancel_appointment or complete_appointment).
        
        Args:
            patient_id: New patient ID (optional)
            practitioner_id: New practitioner ID (optional)
            time_slot: New time slot (optional)
        
        Raises:
            ValueError: If appointment cannot be updated or data is invalid
        """
        if self._status != AppointmentStatus.SCHEDULED:
            raise ValueError(f"Cannot update appointment with status {self._status.value}. Only SCHEDULED appointments can be updated.")
        
        # Validate each field if provided
        if patient_id is not None:
            if patient_id <= 0:
                raise ValueError(f"Invalid patient_id: {patient_id}. Must be positive integer.")
            self._patient_id = patient_id
        
        if practitioner_id is not None:
            if practitioner_id <= 0:
                raise ValueError(f"Invalid practitioner_id: {practitioner_id}. Must be positive integer.")
            self._practitioner_id = practitioner_id
        
        if time_slot is not None:
            if time_slot <= datetime.now():
                raise ValueError(f"Invalid time_slot: {time_slot}. Must be in the future.")
            self._time_slot = time_slot

    def get_status(self) -> AppointmentStatus:
        """
        Returns the current appointment status.
        """
        return self._status

    def is_scheduled(self) -> bool:
        """Returns True if appointment is SCHEDULED."""
        return self._status == AppointmentStatus.SCHEDULED

    def is_completed(self) -> bool:
        """Returns True if appointment is COMPLETED."""
        return self._status == AppointmentStatus.COMPLETED

    def is_cancelled(self) -> bool:
        """Returns True if appointment is CANCELLED."""
        return self._status == AppointmentStatus.CANCELLED