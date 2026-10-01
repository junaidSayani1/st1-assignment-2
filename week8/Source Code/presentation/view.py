from datetime import datetime, timedelta

from domain.models.exceptions import AppointmentSchedulingError, InvalidIdError, InvalidStatusTransitionError
from services.appointment_service import AppointmentService


def format_appointment(details: dict) -> str:
    time_slot = details["time_slot"].strftime("%Y-%m-%d %H:%M")
    return (
        "-------------------------------\n"
        f"id {details['appointment_id']}\n"
        f"patient {details['patient_id']}\n"
        f"practitioner {details['practitioner_id']}\n"
        f"time {time_slot}\n"
        f"status {details['status']}"
    )


def demo(service: AppointmentService) -> None:

    while True:
        choice = input("\n1) Book Appointment \n2) Cancel Appointment \n3) Complete Appointment \n4) Update Appointment \n5) Use Demo Data \nPress 0 to Exit:\n").strip()
        if choice == "0":
            return
        try:
            if choice == "1":
                pt_id = int(input("Patient id: "))
                pr_id = int(input("Practitioner id: "))
                time_str = input("Time: ")
                appointment = service.book_appointment(pt_id, pr_id, datetime.strptime(time_str, "%Y-%m-%d %H:%M"))
                print("Appointment booked successfully:")
                print(format_appointment(appointment.get_appointment_details()))
            elif choice == "2":
                appointment_id = int(input("Appointment id: "))
                appointment = service.cancel_appointment(appointment_id)
                print("Appointment canceled successfully:")
                print(format_appointment(appointment.get_appointment_details()))
            elif choice == "3":
                appointment_id = int(input("Appointment id: "))
                appointment = service.complete_appointment(appointment_id)
                print("Appointment completed successfully:")
                print(format_appointment(appointment.get_appointment_details()))
            elif choice == "4":
                appointment_id = int(input("Appointment id: "))
                pt_id = input("Enter patient Id (Leave blank if no change): ").strip()
                pr_id = input("Enter practitioner Id (Leave blank if no change): ").strip()
                time = input("Enter time (Leave blank if no change): ").strip()
                if pt_id:
                    pt_id = int(pt_id)
                else:
                    pt_id = None
                if pr_id:
                    pr_id = int(pr_id)
                else:
                    pr_id = None
                if time:
                    time = datetime.strptime(time, "%Y-%m-%d %H:%M")
                else:
                    time = None
                appointment = service.update_appointment(appointment_id, pt_id, pr_id, time)
                print("Appointment updated successfully:")
                print(format_appointment(appointment.get_appointment_details()))
            elif choice == "5":
                appointment = service.book_appointment(1, 1, datetime.now()+ timedelta(days=1))
                print("Demo appointment booked.")
                print(format_appointment(appointment.get_appointment_details()))

            else:
                print("Invalid choice. Please try again.")                
        except (AppointmentSchedulingError, InvalidStatusTransitionError, InvalidIdError, ValueError) as error:
            print(error)
