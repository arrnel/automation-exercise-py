from src.client.core.assertion import AssertableResponse
from src.client.core.base_api_client import RestClient
from src.config.config import CFG
from src.model.enum.content_type import ContentType
from src.model.enum.log_level import ApiLogLvl
from src.util.routes import ApiRoutes

CSRF_KEY = "csrfmiddlewaretoken"


class AuthApiClient(RestClient):

    def __init__(self):
        super().__init__(
            base_url=CFG.base_url,
            follow_redirects=True,
            content_type=ContentType.URL_ENCODED,
            api_log_lvl=ApiLogLvl.HEADERS,
        )

    def send_get_csrf_token_request(self) -> AssertableResponse:
        return self.get(ApiRoutes.LOGIN.path())

    def send_login_request(
        self, email: str, password: str, csrf: str
    ) -> AssertableResponse:

        headers = {"Referer": CFG.base_url + ApiRoutes.LOGIN.path()}
        cookies = {CFG.csrf_cookie_title: csrf}
        body = {
            "email": email,
            "password": password,
            CSRF_KEY: csrf,
        }

        return self.post(
            url=ApiRoutes.LOGIN.path(),
            data=body,
            headers=headers,
            cookies=cookies,
        )

    def send_logout_request(self) -> AssertableResponse:
        return self.get(ApiRoutes.LOGOUT.path())
