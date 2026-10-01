from domain.models.exceptions import InvalidIdError, InvalidNameError


class Practitioner:

    def __init__(self, practitioner_id: int, name: str, speciality: str) -> None:
        if name is None or not name.strip():
            raise InvalidNameError()
        self._name = name
        if practitioner_id <= 0:
            raise InvalidIdError("practitioner_id", practitioner_id)
        self._id = practitioner_id
        self._speciality = speciality

    def get_practitioner_details(self) -> dict:
        return {
            "practitioner_id": self._id,
            "name": self._name,
            "speciality": self._speciality
        }

    def set_practitioner_details(self, name: str | None, speciality: str | None) -> None:
        if name is not None:
            if not name.strip():
                raise InvalidNameError()
            self._name = name
        if speciality is not None:
            self._speciality = speciality
