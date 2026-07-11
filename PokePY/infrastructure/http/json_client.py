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

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        allow_not_found: bool = False,
    ) -> dict[str, Any] | list[Any] | None:
        url = self._url(path)
        try:
            response = requests.request(
                method,
                url,
                json=json_body,
                params=params,
                timeout=self.timeout_seconds,
            )
        except requests.RequestException as error:
            raise ApiRequestError(method=method, url=url, message=str(error)) from error

        if allow_not_found and response.status_code == 404:
            return None

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

        if not response.content:
            return {}

        try:
            payload = response.json()
        except ValueError as error:
            raise ApiRequestError(
                method=method,
                url=url,
                message="Resposta da API não é JSON válido.",
                status_code=response.status_code,
                response_body=response.text,
            ) from error

        if not isinstance(payload, (dict, list)):
            raise ApiRequestError(
                method=method,
                url=url,
                message="Resposta JSON da API possui formato inesperado.",
                status_code=response.status_code,
                response_body=response.text,
            )
        return payload

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        response = self.request("GET", path, params=params)
        assert response is not None
        return response

    def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any] | list[Any]:
        response = self.request("POST", path, json_body=payload)
        assert response is not None
        return response

    def put(self, path: str, payload: dict[str, Any]) -> dict[str, Any] | list[Any]:
        response = self.request("PUT", path, json_body=payload)
        assert response is not None
        return response

    def _url(self, path: str) -> str:
        normalized_path = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{normalized_path}"
