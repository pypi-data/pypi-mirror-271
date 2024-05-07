""" Utility functions for package."""
from __future__ import annotations

import inspect
import re
from asyncio import iscoroutine
from decimal import Decimal
from datetime import date
from datetime import datetime
from datetime import timedelta
from functools import partial
from inspect import cleandoc
from json import JSONEncoder
from typing import Callable
from typing import Iterable
from typing import Literal


def iterable_str_arg(s: str | Iterable[str]) -> tuple[str]:
    if isinstance(s, str):
        s = s.replace(",", " ").strip().replace("  ", " ").split()
    return tuple(map(str, s))


def unwrap_func(func: Callable) -> Callable:
    _func = func
    while hasattr(_func, "__wrapped__") or isinstance(_func, partial):
        _func = getattr(_func, "__wrapped__", None) or _func.func
    return _func


def parse_doc_string(s: str) -> dict:
    parsed_doc = {"__doc__": ""}
    doc = cleandoc(s)

    ...

    return parsed_doc


def short_description_by_name(s: str) -> str:
    if isinstance(s, str):
        return re.sub(r"[\.-_]", " ", s).capitalize()


async def invoke(func):
    result = func()
    if iscoroutine(result):
        return await result
    return result


def get_cookies(cookie_str: str) -> dict[str, str]:
    if cookie_str is None:
        return {}

    # it may be a many matches?
    # wsgi_combined_cookie = ";".join(headers.getlist("HTTP_COOKIE"))

    _cookies = {}
    for cookie_item in cookie_str.split(";"):
        if "=" not in cookie_item or "DELETED" in cookie_item:
            continue
        name, value = cookie_item.strip().split("=", 1)
        _cookies[name] = value

    return _cookies


def set_cookie(
    name: str,
    value: str,
    expires: datetime | int | str | None = None,
    max_age: timedelta | int | None = None,
    domain: str | None = None,
    path: str | None = None,
    secure: bool | None = None,
    http_only: bool | None = None,
    same_site: Literal["Strict", "Lax", "None"] | None = None,
    flags: Iterable[str] | None = None,
) -> tuple[str, str]:
    """Returns tuple with cookie values prepared for ASGI/WSGI interface.

    RFC6265: https://datatracker.ietf.org/doc/html/rfc6265

    """
    if "__Secure" in name:
        secure = True
    if "__Host" in name:
        secure = True
        domain = None
        path = "/"
    value = value.replace(";", "")
    if expires:
        if isinstance(expires, int):
            expires = datetime.fromtimestamp(expires)
        if isinstance(expires, datetime):
            expires = expires.strftime("%a, %d %b %Y %H:%M:%S %Z")
        assert isinstance(expires, str)
        value += f"; Expires={expires}"
    if max_age:
        if isinstance(max_age, timedelta):
            max_age = max_age.days * 24 * 3600 + max_age.seconds
        assert isinstance(max_age, int) and max_age > 0
        value += f"; Max-Age={max_age}"
    if isinstance(domain, str):
        value += f"; Domain={domain}"
    if isinstance(path, str):
        value += f"; Path={path}"
    if secure:
        value += "; Secure"
    if http_only:
        value += "; HttpOnly"
    if same_site:
        assert same_site in ("Strict", "Lax", "None")
        if same_site == "None":
            assert secure is True
        value += f"; SameSite={same_site}"
    if flags:
        value += "; " + "; ".join(flags)

    return "Set-Cookie", f"{name}={value}".strip()


def mark_cookie_as_deleted(name: str) -> tuple[str, str]:
    expiry_string = "Thu, 01 Jan 1970 00:00:00 GMT"
    value = "DELETED"
    return "Set-Cookie", f"{name}={value}; Expires={expiry_string}"


def as_headers(cookie_dict: dict[str, str]):
    """start_response("200 OK", self.headers)"""
    _headers = []
    for k, v in cookie_dict.items():
        _headers.append(("Set-Cookie", f"{k}={v}"))
    return _headers


def match_path(item_path: str | re.Pattern[str], path_info: str) -> bool:
    """Check if the `path_info` (CGI) is equal to the given `item_path`
    of the element being checked.

    :param item_path: URL or regex pattern to match against the request path.
    :param path_info: Request path string.
    """

    if item_path is None:
        return True
    if isinstance(item_path, str):
        # or path_info.startswith(item_path) ?
        return path_info == item_path
    if isinstance(item_path, re.Pattern):
        return bool(item_path.match(path_info))

    return False


def check_request(path, entries):
    for pattern in entries:
        if re.match(pattern, path):
            return True

    return False


class DatetimeDecimalEncoder(JSONEncoder):
    """Encoder for datetime and decimal serialization.

    Usage: json.dumps(object, cls=DatetimeDecimalEncoder)
    NOTE: _iterencode does not work

    """

    def default(self, obj) -> str:
        """Encode JSON.

        :return: A JSON encoded string

        """
        if isinstance(obj, Decimal):
            return float(obj)

        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

        return super().default(self, obj)


# validating parameters
def is_invalid_params(func, *args, **kwargs):
    """
    Method:
        Validate pre-defined criteria, if any is True - function is invalid
        0. func should be callable
        1. kwargs should not have unexpected keywords
        2. remove kwargs.keys from func.parameters
        3. number of args should be <= remaining func.parameters
        4. number of args should be >= remaining func.parameters less default
    """
    # For builtin functions inspect.signature(func) return error. If builtin
    # function generates TypeError, it is because of wrong parameters.
    if not inspect.isfunction(func):
        return True

    signature = inspect.signature(func)
    parameters = signature.parameters

    unexpected = set(kwargs.keys()) - set(parameters.keys())
    if len(unexpected) > 0:
        return True

    params = [
        parameter
        for name, parameter in parameters.items()
        if name not in kwargs
    ]
    params_required = [
        param for param in params if param.default is param.empty
    ]

    return not (len(params_required) <= len(args) <= len(params))
