import json
import logging
from typing import Optional, Union

from httpx import Request, Response

from src.model.enum.meta.content_type import ContentType
from src.model.enum.meta.log_level import ApiLogLvl


def format_request(request: Request, api_log_lvl: ApiLogLvl) -> str:
    if api_log_lvl == ApiLogLvl.NONE:
        return ""

    body = None if __body_not_exists(request) else __pretty_body(request)
    base = f"Method: {request.method}\nEndpoint: {request.url}"

    if api_log_lvl == ApiLogLvl.HEADERS:
        return f"{base}\nHeaders: {dict(request.headers)}"
    elif api_log_lvl == ApiLogLvl.BODY:
        return f"{base}\nBody: {body}"
    else:
        return f"{base}\nHeaders: {dict(request.headers)}\nBody: {body}"


def format_response(response: Response, api_log_lvl: ApiLogLvl) -> str:
    if api_log_lvl == ApiLogLvl.NONE:
        return ""

    body = None if __body_not_exists(response) else __pretty_body(response)
    base = f"Status code: {response.status_code}\nEndpoint: {response.url}"

    if api_log_lvl == ApiLogLvl.HEADERS:
        return f"{base}\nHeaders: {dict(response.headers)}"
    elif api_log_lvl == ApiLogLvl.BODY:
        return f"{base}\nBody: {body}"
    else:
        return f"{base}\nHeaders: {dict(response.headers)}\nBody: {body}"


def __body_not_exists(req_res: Request | Response) -> bool:
    try:
        content = req_res.content
    except Exception:
        return True

    return not content


def __pretty_body(req_res: Union[Request, Response]) -> Optional[str]:
    content = req_res.content or b""
    if not content:
        return None

    body = content.decode("utf-8", errors="replace")
    content_type = (req_res.headers.get("Content-Type") or "").lower()

    if content_type in [ContentType.JSON.mime_type, ContentType.GITHUB_JSON.mime_type]:
        return __pretty_json(body)
    elif content_type == ContentType.HTML.mime_type:
        return __pretty_html(body)
    elif content_type in ContentType.URL_ENCODED.mime_type:
        return __pretty_form_urlencoded(body)

    return body


def __pretty_json(body: str) -> str:
    try:
        return json.dumps(json.loads(body), indent=2, ensure_ascii=False)
    except Exception:
        logging.error(f"Unable to pretty print json: {body}", exc_info=True)
        return body


def __pretty_html(body: str) -> str:
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
            f"{k} = {v if len(v) > 1 else v[0] if v else ''}" for k, v in parsed.items()
        ]
        return "Form Data (urlencoded):\n" + "\n".join(lines)
    except Exception:
        logging.error(f"Unable to pretty print form-data: {body}", exc_info=True)
        return body
