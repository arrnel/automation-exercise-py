from abc import ABC

from pydantic import BaseModel, ConfigDict


class Model(BaseModel, ABC):

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        serialize_by_alias=True,
    )
