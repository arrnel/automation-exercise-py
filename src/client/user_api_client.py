from src.client.core.assertion import AssertableResponse
from src.client.core.base_api_client import RestClient
from src.config.config import CFG
from src.mapper.user_mapper import UserMapper
from src.model.enum.meta.content_type import ContentType
from src.model.user import User
from src.util.api.routes import ApiRoutes


class UserApiClient(RestClient):

    def __init__(self):
        super().__init__(
            base_url=CFG.base_api_url,
            content_type=ContentType.URL_ENCODED,
            api_log_lvl=CFG.api_log_lvl,
        )

    def send_create_new_user_request(self, user: User) -> AssertableResponse:
        return self.post(
            url=ApiRoutes.CREATE_USER_ACCOUNT.path(),
            data=UserMapper.to_create_user_request(user).model_dump(exclude_none=True),
        )

    def send_get_user_by_email_request(self, email: str) -> AssertableResponse:
        return self.get(
            url=ApiRoutes.GET_USER_ACCOUNT.path(),
            params={"email": email},
        )

    def send_update_user_request(self, user: User) -> AssertableResponse:
        return self.put(
            url=ApiRoutes.UPDATE_USER_ACCOUNT.path(),
            data=UserMapper.to_update_user_request(user).model_dump(exclude_none=True),
        )

    def send_delete_user_request(self, email: str, password: str) -> AssertableResponse:
        return self.delete(
            url=ApiRoutes.DELETE_USER_ACCOUNT.path(),
            data={
                "email": email,
                "password": password,
            },
        )
