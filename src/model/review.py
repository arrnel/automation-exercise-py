from dataclasses import dataclass


@dataclass
class ReviewInfo:
    name: str
    email: str
    message: str

    def with_name(self, name: str):
        return ReviewInfo(name=name, email=self.email, message=self.message)

    def with_email(self, email: str):
        return ReviewInfo(name=self.name, email=email, message=self.message)

    def with_message(self, message: str):
        return ReviewInfo(name=self.name, email=self.email, message=message)

    def __repr__(self) -> str:
        return f"ReviewInfo(name={self.name!r}, email={self.email!r}, message={self.message!r})"

    def __str__(self) -> str:
        return self.__repr__()
