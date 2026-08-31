# AI_alternative.py
# Beginner-friendly SmartCare booking helper.
# Stores patient name, practitioner name, and appointment time.
# No database. No GUI. Optional save to a plain JSON text file (not a DB).

from datetime import datetime
import json
from pathlib import Path

TIME_FORMAT = "%Y-%m-%d %I:%M %p"  # example: 2024-07-20 10:00 AM
DATA_FILE = Path(__file__).with_name("appointments.json")

appointments = []  # each item: {id, patient, practitioner, time}


def _next_id():
    if not appointments:
        return 1
    return max(item["id"] for item in appointments) + 1


def _normalise_name(text):
    return " ".join(text.strip().split())


def _parse_time(appointment_time):
    cleaned = appointment_time.strip()
    try:
        return datetime.strptime(cleaned, TIME_FORMAT)
    except ValueError:
        raise ValueError(
            "Time must look like 2024-07-20 10:00 AM (YYYY-MM-DD hh:mm AM/PM)."
        )


def _find_clash(practitioner_name, when, ignore_id=None):
    practitioner_key = practitioner_name.casefold()
    for item in appointments:
        if ignore_id is not None and item["id"] == ignore_id:
            continue
        same_gp = item["practitioner"].casefold() == practitioner_key
        same_time = datetime.strptime(item["time"], TIME_FORMAT) == when
        if same_gp and same_time:
            return item
    return None


def store_appointment(patient_name, practitioner_name, appointment_time):
    """Validate, reject clashes, store one appointment, return the record."""
    patient = _normalise_name(patient_name)
    practitioner = _normalise_name(practitioner_name)

    if not patient:
        raise ValueError("Patient name cannot be empty.")
    if not practitioner:
        raise ValueError("Practitioner name cannot be empty.")

    when = _parse_time(appointment_time)
    clash = _find_clash(practitioner, when)
    if clash:
        raise ValueError(
            f"{practitioner} already has a booking at {clash['time']} "
            f"(patient: {clash['patient']})."
        )

    record = {
        "id": _next_id(),
        "patient": patient,
        "practitioner": practitioner,
        "time": when.strftime(TIME_FORMAT),
    }
    appointments.append(record)
    return record


def cancel_appointment(appointment_id):
    """Remove a booking by its number. Returns True if it was found."""
    for index, item in enumerate(appointments):
        if item["id"] == appointment_id:
            appointments.pop(index)
            return True
    return False


def reschedule_appointment(appointment_id, new_time):
    """Change the time of an existing booking, still blocking clashes."""
    target = None
    for item in appointments:
        if item["id"] == appointment_id:
            target = item
            break
    if target is None:
        raise ValueError(f"No appointment with id {appointment_id}.")

    when = _parse_time(new_time)
    clash = _find_clash(target["practitioner"], when, ignore_id=appointment_id)
    if clash:
        raise ValueError(
            f"{target['practitioner']} already has a booking at {clash['time']}."
        )
    target["time"] = when.strftime(TIME_FORMAT)
    return target


def show_appointments():
    """Print every stored appointment, ordered by time."""
    if not appointments:
        print("No appointments stored.")
        return
    ordered = sorted(
        appointments,
        key=lambda item: datetime.strptime(item["time"], TIME_FORMAT),
    )
    print("ID | Patient | Practitioner | Time")
    print("-" * 56)
    for item in ordered:
        print(
            f"{item['id']} | {item['patient']} | "
            f"{item['practitioner']} | {item['time']}"
        )


def save_appointments():
    """Write the list to a JSON file so bookings survive closing the program."""
    DATA_FILE.write_text(json.dumps(appointments, indent=2), encoding="utf-8")
    print(f"Saved {len(appointments)} appointment(s) to {DATA_FILE.name}.")


def load_appointments():
    """Read bookings back from the JSON file if it exists."""
    global appointments
    if not DATA_FILE.exists():
        return
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    appointments = data if isinstance(data, list) else []


def seed_sample_bookings():
    """Add the two lab sample bookings if the list is still empty."""
    if appointments:
        return
    store_appointment("Alice Smith", "Dr. John Doe", "2024-07-20 10:00 AM")
    store_appointment("Bob Johnson", "Dr. Jane Roe", "2024-07-20 11:30 AM")


def _read_line(prompt):
    return input(prompt).strip()


def run_menu():
    print("SmartCare booking helper (console only: no database, no GUI)")
    print("Time format: 2024-07-20 10:00 AM")
    load_appointments()
    if not appointments:
        seed_sample_bookings()
        print("Started with two sample bookings.\n")
    else:
        print(f"Loaded {len(appointments)} booking(s) from file.\n")

    while True:
        print("1 Book  2 List  3 Cancel  4 Reschedule  5 Save  6 Quit")
        choice = _read_line("Choose: ")
        try:
            if choice == "1":
                store_appointment(
                    _read_line("Patient name: "),
                    _read_line("Practitioner name: "),
                    _read_line("Appointment time: "),
                )
                print("Booked.\n")
            elif choice == "2":
                show_appointments()
                print()
            elif choice == "3":
                appointment_id = int(_read_line("Appointment ID to cancel: "))
                if cancel_appointment(appointment_id):
                    print("Cancelled.\n")
                else:
                    print("That ID was not found.\n")
            elif choice == "4":
                appointment_id = int(_read_line("Appointment ID to reschedule: "))
                reschedule_appointment(
                    appointment_id,
                    _read_line("New time: "),
                )
                print("Rescheduled.\n")
            elif choice == "5":
                save_appointments()
                print()
            elif choice == "6":
                print("Goodbye.")
                break
            else:
                print("Please choose 1-6.\n")
        except ValueError as error:
            print(f"Could not complete that step: {error}\n")


if __name__ == "__main__":
    run_menu()
