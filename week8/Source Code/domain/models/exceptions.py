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
