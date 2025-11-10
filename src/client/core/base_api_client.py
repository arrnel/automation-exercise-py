import logging
import typing
from abc import ABC
from http import HTTPMethod
from typing import Union

import allure
import httpx
from allure_commons.types import AttachmentType
from httpx import Response, Request, URL
from httpx._client import UseClientDefault
from httpx._types import (
    QueryParamTypes,
    HeaderTypes,
    CookieTypes,
    AuthTypes,
    TimeoutTypes,
    RequestExtensions,
    RequestContent,
    RequestData,
    RequestFiles,
)

from src.client.core.assertion import AssertableResponse
from src.config.config import CFG
from src.model.enum.content_type import ContentType
from src.model.enum.log_level import ApiLogLvl, LogLvl
from src.util.httpx_log_formatter_util import format_request, format_response
from src.util.step_logger import step_log


class RestClient(ABC):

    USE_CLIENT_DEFAULT = UseClientDefault()

    def __init__(
        self,
        base_url: str,
        content_type: ContentType = ContentType.JSON,
        user_agent: str = CFG.default_user_agent,
        http2: bool = False,
        follow_redirects: bool = True,
        api_log_lvl: ApiLogLvl = CFG.api_log_lvl,
        log_lvl: LogLvl = CFG.log_lvl,
        timeout: float = CFG.http_timeout,
    ):
        self._base_url = base_url
        self._follow_redirects = follow_redirects
        self._content_type = content_type
        self._api_log_lvl = api_log_lvl
        self._log_lvl = log_lvl

        headers = {"Content-Type": content_type.mime_type}
        if user_agent is not None:
            headers["User-Agent"] = user_agent

        self._client = httpx.Client(
            base_url=base_url,
            follow_redirects=follow_redirects,
            http2=http2,
            headers=headers,
            timeout=timeout,
        )

    def get(self, url: URL | str, **kwargs):
        return self.__send(HTTPMethod.GET, url, **kwargs)

    def post(self, url: URL | str, **kwargs):
        return self.__send(HTTPMethod.POST, url, **kwargs)

    def put(self, url: URL | str, **kwargs):
        return self.__send(HTTPMethod.PUT, url, **kwargs)

    def patch(self, url: URL | str, **kwargs):
        return self.__send(HTTPMethod.PATCH, url, **kwargs)

    def delete(self, url: URL | str, **kwargs):
        return self.__send(HTTPMethod.DELETE, url, **kwargs)

    def __send(
        self,
        method: HTTPMethod,
        url: URL,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
    ):
        with step_log.log(f"Send request [{method.name}]: {url}"):
            try:
                response = self._client.request(
                    method=method.name,
                    url=url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                    follow_redirects=follow_redirects,
                    timeout=timeout,
                    extensions=extensions,
                )

                self.__log_and_attach(response.request)
                self.__log_and_attach(response)

                return AssertableResponse(response)

            except httpx.HTTPError as e:
                logging.exception(f"HTTP request failed: {e}")
                raise

    def __log_and_attach(
        self,
        req_res: Union[Request, Response],
        attachment_type: AttachmentType = AttachmentType.TEXT,
    ):
        if isinstance(req_res, Request):
            title = "Request"
            log = format_request(req_res, self._api_log_lvl)
        else:
            title = "Response"
            log = format_response(req_res, self._api_log_lvl)
        logging.log(self._log_lvl.code, f"{title}\n\n{log}\n")
        allure.attach(log, title, attachment_type)
