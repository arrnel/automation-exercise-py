from dataclasses import dataclass


@dataclass
class AddressInfo:
    title: str
    full_name: str
    company: str
    address1: str
    address2: str
    city_state_zip: str
    country: str
    phone_number: str

    def __repr__(self) -> str:
        return (
            f"AddressInfo(title={self.title!r}, full_name={self.full_name!r}, company={self.company!r}, "
            f"address1={self.address1!r}, address2={self.address2!r}, city_state_zip={self.city_state_zip!r}, "
            f"country={self.country!r}, phone_number={self.phone_number!r})"
        )

    def __str__(self) -> str:
        return self.__repr__()
