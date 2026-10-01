from datetime import datetime
from domain.models.appointment import Appointment, AppointmentStatus
from domain.models.exceptions import AppointmentSchedulingError
from repositories.appointment_repository import AppointmentRepository


class AppointmentService:

    def __init__(self, repository: AppointmentRepository) -> None:
        self._repository = repository
        self._last_id = 0
        
        for appointment in self._repository.find_all():
            appointment_id = appointment.get_appointment_details()["appointment_id"]
            
            if appointment_id > self._last_id:
                self._last_id = appointment_id

    def book_appointment(self, patient_id: int, practitioner_id: int, time_slot: datetime) -> Appointment:
        
        self.check_time(time_slot)
       
        self.conflict_check(patient_id, practitioner_id, time_slot)
        appointment_id = self._last_id + 1
        
        appointment = Appointment(appointment_id, patient_id, practitioner_id, time_slot)
        self._repository.save(appointment)
        self._last_id = appointment_id
        return appointment

    def cancel_appointment(self, appointment_id: int) -> Appointment:
        appointment = self._repository.find_by_id(appointment_id)
       
        if appointment is None:
            raise AppointmentSchedulingError(f"Appointment not found: {appointment_id}.")
        
        appointment.cancel_appointment()
        
        self._repository.save(appointment)
        
        return appointment

    def complete_appointment(self, appointment_id: int) -> Appointment:
    
        appointment = self._repository.find_by_id(appointment_id)
    
        if appointment is None:
            raise AppointmentSchedulingError(f"Appointment not found: {appointment_id}.")
    
        appointment.complete_appointment()
    
        self._repository.save(appointment)
    
        return appointment

    def update_appointment(self, appointment_id: int, patient_id: int | None = None, practitioner_id: int | None = None, 
                           time_slot: datetime | None = None) -> Appointment:
        
        appointment = self._repository.find_by_id(appointment_id)
       
        if appointment is None:
            raise AppointmentSchedulingError(f"Appointment not found: {appointment_id}.")

        if time_slot is not None:
            self.check_time(time_slot)

        details = appointment.get_appointment_details()
        if patient_id is None:
            new_patient_id = details["patient_id"]
        else:
            new_patient_id = patient_id

        if practitioner_id is None:
            new_practitioner_id = details["practitioner_id"]
        else:
            new_practitioner_id = practitioner_id

        if time_slot is None:
            new_time_slot = details["time_slot"]
        else:
            new_time_slot = time_slot

        self.conflict_check(new_patient_id, new_practitioner_id, new_time_slot, appointment_id)

        appointment.update_appointment(patient_id, practitioner_id, time_slot)
        
        self._repository.save(appointment)
        
        return appointment

    def check_time(self, time_slot: datetime) -> None:
        if time_slot <= datetime.now():
            raise AppointmentSchedulingError(f"Invalid time_slot: {time_slot}. Must be in the future.")

    def conflict_check(self, patient_id: int, practitioner_id: int, time_slot: datetime, appointment_id: int | None = None) -> None:
        appointments = self._repository.find_all()
        for appointment in appointments:
            
            details = appointment.get_appointment_details()

            if details["appointment_id"] == appointment_id or details["status"] != AppointmentStatus.SCHEDULED.value or details["time_slot"] != time_slot:
                continue
            
            if details["patient_id"] == patient_id:
                raise AppointmentSchedulingError(f"Patient with ID: {patient_id} already has an appointment at {time_slot}.")
            
            if details["practitioner_id"] == practitioner_id:
                raise AppointmentSchedulingError(f"Practitioner with ID: {practitioner_id} already has an appointment at {time_slot}.")