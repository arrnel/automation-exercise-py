from src.client.core.assertion import AssertableResponse
from src.client.core.base_api_client import RestClient
from src.config.config import CFG
from src.model.dto.user.credentials_request import CredentialsRequestDTO
from src.model.enum.meta.content_type import ContentType
from src.util.api.routes import ApiRoutes


class AuthApiClient(RestClient):

    def __init__(self):
        super().__init__(
            base_url=CFG.base_url,
            follow_redirects=True,
            content_type=ContentType.URL_ENCODED,
            api_log_lvl=CFG.api_log_lvl,
        )

    def send_get_csrf_token_request(self) -> AssertableResponse:
        return self.get(ApiRoutes.LOGIN.path())

    def send_login_request(
        self, email: str, password: str, csrf: str
    ) -> AssertableResponse:
        return self.post(
            url=ApiRoutes.LOGIN.path(),
            headers={"Referer": CFG.base_url + ApiRoutes.LOGIN.path()},
            data=CredentialsRequestDTO(
                csrf=csrf, email=email, password=password
            ).model_dump(exclude_none=True),
        )

    def send_logout_request(self) -> AssertableResponse:
        return self.get(ApiRoutes.LOGOUT.path())
