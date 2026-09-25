from datetime import datetime, timedelta
from enum import Enum

class Patient:
    pass

class Appointment:
    pass

class Practitioner:
    pass


class AppointmentStatus(Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class AppointmentSchedulingError(Exception):

    def __init__(self, message: str) -> None:
        super().__init__(message)

class InvalidStatusTransitionError(Exception):

    def __init__(self, transition: str, current_status: str) -> None:
        super().__init__(
            f"Cannot {transition} an appointment with status: {current_status}."
        )

class InvalidNameError(Exception):

    def __init__(self) -> None:
        super().__init__("Name cannot be empty.")

class InvalidEmailError(Exception):
    pass

class InvalidIdError(Exception):

    def __init__(self, id_name: str, value: int) -> None:
        super().__init__(f"Invalid {id_name}: {value}. Must be a positive integer.")


class Practitioner:

    """
    Practitioner class represents a healthcare practitioner in the system.
    """

    def __init__(self, practitioner_id: int, name: str, speciality: str) -> None:
        """
        Initialize a Practitioner object with validation.
        Args:

            practitioner_id: Unique practitioner identifier (must be positive)  
            name: Name of the practitioner (must not be empty)
            speciality: Speciality of the practitioner (must not be empty)
        
        Raises:
            InvalidNameError: If the name is empty or missing.
            InvalidIdError: If the practitioner_id is not a positive integer.
        """

        if name is None or not name.strip():
            raise InvalidNameError()

        self._name = name

        if practitioner_id <= 0:
            raise InvalidIdError("practitioner_id", practitioner_id)

        self._id = practitioner_id
        self._speciality = speciality

        return

    def get_practitioner_details(self) -> dict:
        """
        Simple getter function
        Returns:
          practitioner details as a dictionary.
        """
        return {
            "practitioner_id": self._id,
            "name": self._name,
            "speciality": self._speciality
        }

    def set_practitioner_details(self, name: str | None, speciality: str | None) -> None:

        """
        Update practitioner details with validation.

        Args:
            name: New name for the practitioner (optional)
            speciality: New speciality for the practitioner (optional)
        """
        if name is not None:
            if not name.strip():
                raise InvalidNameError()
            self._name = name

        if speciality is not None:
            self._speciality = speciality

        return

class Patient:
    """
    Patient class represents a patient in the healthcare system.
    It encapsulates patient details and provides methods to access and update them (getters and setters).
    """

    def __init__(self, patient_id: int, name: str, email: str, medical_history: list[str] | None = None) -> None:

        """
        Initialize a Patient object with validation.

        Args:
            patient_id: Unique patient identifier (must be positive)
            name: Name of the patient (must not be empty)
            email: Email of the patient (must contain @ and .)
            medical_history: Optional list of medical history entries (default: None)
        
        Raises:
            InvalidNameError: If the name is empty or missing.
            InvalidIdError: If the patient_id is not a positive integer.
            InvalidEmailError: If the email is invalid.
    
        """
        
        self.validate_details(patient_id, name, email)

        self._id = patient_id
        self._name = name
        self._email = email
        if medical_history is None:
            self._medical_history = []
        else:
            self._medical_history = medical_history

    def get_patient_details(self) -> dict:

        """
        Returns:
          patient details as a dictionary.
        """
        return {
            "patient_id": self._id,
            "name": self._name,
            "email": self._email
        }

    def update_patient_details(self, name: str, email: str, medical_history: list[str] | None) -> None:

        """
        Update patient details with validation.
        Args:
            name: New name for the patient (must not be empty)
            email: New email for the patient (must contain @ and .)
            medical_history: Optional new list of medical history entries
        Raises:
            InvalidNameError: If the name is empty or missing.
            InvalidIdError: If the patient_id is not a positive integer.
            InvalidEmailError: If the email is invalid.
        """

        self.validate_details(patient_id=self._id, name = name, email = email)
        self._name = name 
        self._email = email
        if medical_history is not None:
            self._medical_history = medical_history

        return

    def get_medical_history(self) -> list[str]:
        """
        Returns:
          The patient's medical history as a new list.
        """
        medical_history_temp = list(self._medical_history)
        return medical_history_temp 
    

    def validate_details(self, patient_id: int, name: str, email: str) -> None:

        """
        Patient specific validation method that enforces all Patient invariants.
        
        Raises:
            InvalidNameError: If the name is empty or missing.
            InvalidIdError: If the patient_id is not a positive integer.
            InvalidEmailError: If the email is invalid.
        """
        if patient_id <= 0:
            raise InvalidIdError("patient_id", patient_id)
        
        if not name or not name.strip():
            raise InvalidNameError()
        
        if "@" not in email or "." not in email:
            raise InvalidEmailError(f"{email} is not in valid format.")

        return





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
            InvalidIdError: If any ID is not a positive integer
            AppointmentSchedulingError: If any invariant is violated
        """
        if appointment_id <= 0:
            raise InvalidIdError("appointment_id", appointment_id)
        
        if patient_id <= 0:
            raise InvalidIdError("patient_id", patient_id)
        
        if practitioner_id <= 0:
            raise InvalidIdError("practitioner_id", practitioner_id)
        
        if time_slot <= datetime.now():
            raise AppointmentSchedulingError(f"Invalid time_slot: {time_slot}. Must be in the future.")

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
            InvalidStatusTransitionError: If appointment cannot be cancelled from current state
        """
        if self._status == AppointmentStatus.COMPLETED:
            raise InvalidStatusTransitionError("cancel", self._status.value)
        
        if self._status == AppointmentStatus.CANCELLED:
            raise InvalidStatusTransitionError("cancel", self._status.value)
        
        # SCHEDULED → CANCELLED (valid transition)
        self._status = AppointmentStatus.CANCELLED

    def complete_appointment(self) -> None:
        """
        Mark the appointment as completed.
        
        Decision: Only SCHEDULED appointments can be completed.
        This method is added because completion is a valid
        state transition that should be protected like cancellation.
        
        Raises:
            InvalidStatusTransitionError: If appointment cannot be completed from current state
        """
        if self._status == AppointmentStatus.CANCELLED:
            raise InvalidStatusTransitionError("complete", self._status.value)
        
        if self._status == AppointmentStatus.COMPLETED:
            raise InvalidStatusTransitionError("complete", self._status.value)
        
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
            InvalidStatusTransitionError: If appointment cannot be updated from current state
            ValueError: If updated data is invalid
        """
        if self._status != AppointmentStatus.SCHEDULED:
            raise InvalidStatusTransitionError("update", self._status.value)
        
        # Validate each field if provided
        if patient_id is None:
            patient_id = self._patient_id

        if practitioner_id is None:
            practitioner_id = self._practitioner_id

        if time_slot is None:
            time_slot = self._time_slot
                
        self.validate_details(self._id, patient_id, practitioner_id, time_slot)
           
        self._patient_id = patient_id
        self._practitioner_id = practitioner_id
        self._time_slot = time_slot

    def get_status(self) -> AppointmentStatus:
        """
        Returns the current appointment status.
        """
        return self._status



def main() -> None:

    slot = datetime.now() + timedelta(days=1)

    #i m trying to initialize valid patient, practitioner and appointment instances and print to check the happy flow, true case.

    patient = Patient(1, "Junaid", "joji@gmail.com", ["stress"])
    practitioner = Practitioner(3, "Dr. Junaid", "Neurologist")
    appointment = Appointment(2, 1, 3, slot)
    print("Valid patient:", patient.get_patient_details())
    print("Valid practitioner:", practitioner.get_practitioner_details())
    print("Valid appointment:", appointment.get_appointment_details())

    # here i am trying to initialize invalid instances and catching errors.

    try:
        Patient(1, " ", "whatemail", None)
    except InvalidIdError as error:
        print("Invalid patient id:", error)
    except InvalidNameError as error:
        print("Invalid patient name:", error)
    except InvalidEmailError as error:
        print("Invalid patient email:", error)



    try:
        Patient(1, "Junaid", "invalid-email", None)
    except InvalidEmailError as error:
        print("Invalid patient email:", error)


    try:
        Practitioner(-1, "Dr. Invalid", "")
    except InvalidIdError as error:
        print("Invalid practitioner id:", error)


    try:
        Appointment(1, 1, 1, datetime.now() - timedelta(days=1))
    except AppointmentSchedulingError as error:
        print("Invalid appointment:", error)


    appointment.cancel_appointment()

    print("After cancellation:", appointment.get_status().value)

    #trying invalid transition, cancelling an already cancelled appointment
    try:
        appointment.cancel_appointment()
    except InvalidStatusTransitionError as error:
        print("Illegal repeated transition rejected:", error)


if __name__ == "__main__":
    main()

