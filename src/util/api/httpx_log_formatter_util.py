import json
import logging
from typing import Optional, Union

from httpx import Request, Response, RequestNotRead

from src.model.enum.meta.content_type import ContentType
from src.model.enum.meta.log_level import ApiLogLvl


def format_request(request: Request, api_log_lvl: ApiLogLvl) -> Optional[str]:
    message = ""
    if api_log_lvl == ApiLogLvl.NONE:
        return None
    elif api_log_lvl == ApiLogLvl.HEADERS:
        message = f"Method: {request.method}\nEndpoint: {request.url}\nHeaders: {dict(request.headers)}"
    elif api_log_lvl == ApiLogLvl.BODY and request.content:
        message = f"Method: {request.method}\nEndpoint: {request.url}\nBody: {__pretty_body(request)}"
    elif api_log_lvl == ApiLogLvl.ALL:
        message = (
            f"Method: {request.method}\n"
            f"Endpoint: {request.url}\n"
            f"Headers: {dict(request.headers)}\n"
            f"Body: {__pretty_body(request)}"
        )
    return message


def format_response(response: Response, api_log_lvl: ApiLogLvl) -> Optional[str]:
    message = ""
    if api_log_lvl == ApiLogLvl.NONE:
        return None
    elif api_log_lvl == ApiLogLvl.HEADERS:
        message = f"Status code: {response.status_code}\nEndpoint: {response.url}\nHeaders: {dict(response.headers)}"
    elif api_log_lvl == ApiLogLvl.BODY and response.content:
        message = f"Status code: {response.status_code}\nEndpoint: {response.url}\nBody: {__pretty_body(response)}"
    elif api_log_lvl == ApiLogLvl.ALL:
        message = (
            f"Status code: {response.status_code}\n"
            f"Endpoint: {response.url}\n"
            f"Headers: {dict(response.headers)}\n"
            f"Body: {__pretty_body(response)}"
        )
    return message


def __pretty_body(req_res: Union[Request, Response]) -> Optional[str]:

    content_type = req_res.headers.get("Content-Type", "")

    if isinstance(req_res, Request):
        try:
            req_res.read()  # Need for request
            content = req_res.content or b""
        except RequestNotRead:
            content = b""
    else:
        content = req_res.content or b""

    if not content_type or not content:
        return None

    body = content.decode("utf-8", errors="replace")

    match content_type.lower():
        case ContentType.JSON.mime_type:
            return __pretty_json(body)
        case ContentType.HTML.mime_type:
            return __pretty_html(body)
        case _:
            return body


def __pretty_json(body: str) -> str:
    try:
        return json.dumps(json.loads(body), indent=2, ensure_ascii=False)
    except Exception:
        logging.error(f"Unable to pretty print json: {body}", exc_info=True)
        return body


def __pretty_html(body: str) -> str:
    from bs4 import BeautifulSoup

    return BeautifulSoup(body, "html.parser").prettify()
