from dataclasses import dataclass, replace


@dataclass
class TestData:

    session_id: str | None
    csrf: str | None
    password: str | None
    phone_number: str | None

    @classmethod
    def empty(cls) -> "TestData":
        return TestData(session_id=None, csrf=None, password=None, phone_number=None)

    def with_session_id(self, session_id: str):
        return replace(self, session_id=session_id)

    def with_csrf(self, csrf: str):
        return replace(self, csrf=csrf)

    def with_password(self, password: str):
        return replace(self, password=password)

    def with_phone(self, phone: str):
        return replace(self, phone_number=phone)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"session_id={self.session_id!r}, "
            f"csrf={self.csrf!r}, "
            f"password={self.password!r}, "
            f"phone={self.phone_number!r}"
            ")"
        )

    def __str__(self) -> str:
        return self.__repr__()
