from dataclasses import dataclass


@dataclass
class ContactInfo:
    name: str
    email: str
    subject: str
    message: str
    path_to_file: str

    def __repr__(self) -> str:
        return (
            f"ContactInfo(name={self.name!r}, email={self.email!r}, subject={self.subject!r}, "
            f"message={self.message!r}, path_to_file={self.path_to_file!r})"
        )

    def __str__(self) -> str:
        return self.__repr__()
