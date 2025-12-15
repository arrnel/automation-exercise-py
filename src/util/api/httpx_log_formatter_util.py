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
    content_type = req_res.headers.get("Content-Type", None)

    if content_type is None:
        return None

    try:
        if isinstance(req_res, Request):
            req_res.read()
        content = req_res.content or b""
    except RequestNotRead:
        content = b""

    if not content:
        return None

    body = content.decode("utf-8", errors="replace")

    if ContentType.JSON.mime_type in content_type or "text/json" in content_type:
        return __pretty_json(body)

    elif ContentType.HTML.mime_type in content_type:
        return __pretty_html(body)

    elif ContentType.URL_ENCODED.mime_type in content_type:
        return __pretty_form_urlencoded(body)

    else:
        return body


def __pretty_json(body: str) -> str:
    try:
        return json.dumps(json.loads(body), indent=2, ensure_ascii=False)
    except Exception:
        logging.error(f"Unable to pretty print json: {body}", exc_info=True)
        return body


def __pretty_html(body: str) -> str:
    from bs4 import BeautifulSoup
    try:
        from bs4 import BeautifulSoup
        return BeautifulSoup(body, "html.parser").prettify()
    except Exception:
        logging.error(f"Unable to pretty print html: {body}", exc_info=True)
        return body


def __pretty_form_urlencoded(body: str) -> str:
    try:
        from urllib.parse import parse_qs
        parsed = parse_qs(body, keep_blank_values=True, strict_parsing=False)
        lines = [
            f"{k} = {v if len(v) > 1 else v[0] if v else ''}"
            for k, v in parsed.items()
        ]
        return "Form Data (urlencoded):\n" + "\n".join(lines)
    except Exception:
        logging.error(f"Unable to pretty print form-data: {body}", exc_info=True)
        return body
