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
            f"{self.__class__.__name__}("
            f"title={self.title!r}, "
            f"full_name={self.full_name!r}, "
            f"company={self.company!r}, "
            f"address1={self.address1!r}, "
            f"address2={self.address2!r}, "
            f"city_state_zip={self.city_state_zip!r}, "
            f"country={self.country!r}, "
            f"phone_number={self.phone_number!r}"
            ")"
        )

    def __str__(self) -> str:
        return self.__repr__()
