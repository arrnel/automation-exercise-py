from http import HTTPStatus

from src.client.auth_api_client import AuthApiClient
from src.client.core.condition.conditions import Conditions
from src.config.config import CFG
from src.util.decorator.step_logger import step_log
from src.util.store.cookie_store import ThreadSafeCookieStore


class AuthApiService:

    def __init__(self):
        self.auth_api_client = AuthApiClient()

    @step_log.log("Sign in by email = [{email}] and password = [{password}]")
    def sign_in(self, email: str, password: str) -> dict[str, str]:
        self.auth_api_client.send_get_csrf_token_request().check(
            Conditions.status_code(HTTPStatus.OK)
        )

        self.auth_api_client.send_login_request(
            email=email,
            password=password,
            csrf=ThreadSafeCookieStore().get_cookie(CFG.csrf_cookie_title),
        ).check(Conditions.status_code(HTTPStatus.OK))
        return ThreadSafeCookieStore().get_cookies(
            CFG.csrf_cookie_title, CFG.session_id_cookie_title
        )

    @step_log.log("Sign in by email = [{email}] and password = [{password}]")
    def logout(self) -> None:
        self.auth_api_client.send_logout_request().check(
            Conditions.status_code(HTTPStatus.OK)
        )
