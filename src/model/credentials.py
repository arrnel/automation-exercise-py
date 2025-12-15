from dataclasses import dataclass


@dataclass
class Credentials:
    email: str | None
    password: str | None

    def __repr__(self) -> str:
        return f"CredentialsDTO(email={self.email!r}, password={self.password!r})"

    def __str__(self) -> str:
        return self.__repr__()
