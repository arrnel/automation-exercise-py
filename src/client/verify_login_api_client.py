from src.client.core.base_api_client import RestClient
from src.config.config import CFG
from src.model.enum.meta.content_type import ContentType
from src.util.api.routes import ApiRoutes


class VerifyLoginApiClient(RestClient):

    def __init__(self):
        super().__init__(
            base_url=CFG.base_api_url,
            content_type=ContentType.URL_ENCODED,
        )

    def send_verify_login_request(self, email: str, password: str):
        return self.post(
            url=ApiRoutes.VERIFY_LOGIN.path(),
            data={
                "email": email,
                "password": password,
            },
        )
