from src.model.base_model import Model


class CredentialsDTO(Model):
    email: str
    password: str

    def __repr__(self) -> str:
        return f"CredentialsDTO(email={self.email!r}, password={self.password!r})"

    def __str__(self) -> str:
        return self.__repr__()
