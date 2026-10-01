from domain.models.exceptions import InvalidEmailError, InvalidIdError, InvalidNameError


class Patient:

    def __init__(self, patient_id: int, name: str, email: str, medical_history: list[str] | None = None) -> None:
        self.validate_details(patient_id, name, email)
        self._id = patient_id
        self._name = name
        self._email = email
        if medical_history is None:
            self._medical_history = []
        else:
            self._medical_history = medical_history

    def get_patient_details(self) -> dict:
        return {
            "patient_id": self._id,
            "name": self._name,
            "email": self._email
        }

    def update_patient_details(self, name: str, email: str, medical_history: list[str] | None) -> None:
        self.validate_details(patient_id=self._id, name=name, email=email)
        self._name = name
        self._email = email
        if medical_history is not None:
            self._medical_history = medical_history

    def get_medical_history(self) -> list[str]:
        return list(self._medical_history)

    def validate_details(self, patient_id: int, name: str, email: str) -> None:
        if patient_id <= 0:
            raise InvalidIdError("patient_id", patient_id)
        if not name or not name.strip():
            raise InvalidNameError()
        if "@" not in email or "." not in email:
            raise InvalidEmailError(f"{email} is not in valid format.")
