from src.model.category import Category
from src.model.dto.product.product_category_response import CategoryResponseDTO
from src.model.dto.user.user_type import UserTypeDTO


class CategoryMapper:

    @staticmethod
    def to_dto(source: Category) -> CategoryResponseDTO:
        return CategoryResponseDTO(
            category=source.title,
            usertype=UserTypeDTO(usertype=source.user_type)
        )

    @staticmethod
    def to_category(source: CategoryResponseDTO) -> Category:
        return Category(
            user_type=source.usertype.usertype,
            title=source.category,
        )
