from src.model.brand import Brand
from src.model.dto.brand_response import BrandResponseDTO


class BrandMapper:

    @staticmethod
    def to_brand(source: BrandResponseDTO) -> Brand:
        return Brand(
            id=source.id,
            title=source.brand,
        )
