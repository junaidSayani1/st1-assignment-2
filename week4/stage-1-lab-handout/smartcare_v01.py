if __name__ == "__main__":
    print("Welcome to SmartCare: Community Clinic Appointment Booking System!")
    # First Appointment
    patient1_name = 'Alice Smith'
    practitioner1_name = 'Dr. John Doe'
    appointment1_time = '2024-07-20 10:00 AM'
    print(f"Patient: {patient1_name} | Practitioner: {practitioner1_name} | Time: {appointment1_time}")
    # Second Appointment
    patient2_name = 'Bob Johnson'
    practitioner2_name = 'Dr. Jane Roe'
    appointment2_time = '2024-07-20 11:30 AM'
    print(f"Patient: {patient2_name} | Practitioner: {practitioner2_name} | Time: {appointment2_time}")
    print("\n\n\n")
    pt_name = input("Enter Patient's Name: ")
    if not pt_name:
        raise ValueError("Patient Name cannot be empty")
    practioner_name = input("Enter Practitioner's Name: ")
    appointment_time = input("Enter Appointment Time: ")

    print(f"Patient: {pt_name} | Practitioner: {practioner_name} | Time: {appointment_time}")

'''
Answering Questions:

Q) What data must be stored?

A) Data related to patient's name, practitioner's name, appointment time, also practitioners count, 
to reallocate to different gp's. 


Q) What functions might be useful?

A) Functions of booking for an appointment/scheduling, also function to check conflicts, function to check available slots.
Also func to display the complete list/output.


Q) What could go wrong?

A) No typecasting, no try-catching of errors, no input validation, no conflict management. No reallocation for conflicts.


Q) What requirements are unclear?

A) Does the input run forever, or is there a limit of for example 5 appointments per day, and so on.

'''
