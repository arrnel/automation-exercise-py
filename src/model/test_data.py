from dataclasses import dataclass


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
        return TestData(session_id=session_id, csrf=self.csrf, password=self.password, phone_number= self.phone_number)

    def with_csrf(self, csrf: str):
        return TestData(session_id=self.session_id, csrf=csrf, password=self.password, phone_number= self.phone_number)

    def with_password(self, password: str):
        return TestData(session_id=self.session_id, csrf=self.csrf, password=password, phone_number= self.phone_number)

    def with_phone(self, phone: str):
        return TestData(session_id=self.session_id, csrf=self.csrf, password=self.password, phone_number= phone)

    def __repr__(self) -> str:
        return (
            f"TestData(session_id={self.session_id!r}, csrf={self.csrf!r}, "
            f"password={self.password!r}, phone={self.phone_number!r})"
        )

    def __str__(self) -> str:
        return self.__repr__()
