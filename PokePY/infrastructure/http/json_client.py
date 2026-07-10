from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class ApiRequestError(Exception):
    method: str
    url: str
    message: str
    status_code: int | None = None
    response_body: str | None = None

    def __str__(self) -> str:
        status = f" HTTP {self.status_code}" if self.status_code else ""
        body = f" Body: {self.response_body[:300]}" if self.response_body else ""
        return f"{self.method} {self.url}{status}: {self.message}{body}"


class HttpJsonClient:
    def __init__(self, base_url: str, timeout_seconds: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def get(self, path: str, params: dict | None = None) -> dict | list:
        return self._request("GET", path, params=params)

    def post(self, path: str, payload: dict) -> dict | list:
        return self._request("POST", path, json=payload)

    def put(self, path: str, payload: dict) -> dict | list:
        return self._request("PUT", path, json=payload)

    def _request(self, method: str, path: str, **kwargs: Any) -> dict | list:
        url = self._url(path)
        try:
            response = requests.request(method, url, timeout=self.timeout_seconds, **kwargs)
        except requests.RequestException as error:
            raise ApiRequestError(method=method, url=url, message=str(error)) from error

        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            raise ApiRequestError(
                method=method,
                url=url,
                message=str(error),
                status_code=response.status_code,
                response_body=response.text,
            ) from error

        try:
            return response.json()
        except ValueError as error:
            raise ApiRequestError(
                method=method,
                url=url,
                message="Resposta da API não é JSON válido.",
                status_code=response.status_code,
                response_body=response.text,
            ) from error

    def _url(self, path: str) -> str:
        normalized_path = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{normalized_path}"
