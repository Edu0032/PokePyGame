import requests

class HttpJsonClient:
    def __init__(self, base_url: str, timeout_seconds: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def get(self, path: str, params: dict | None = None) -> dict | list:
        response = requests.get(self._url(path), params=params, timeout=self.timeout_seconds)
        response.raise_for_status()
        return response.json()

    def post(self, path: str, payload: dict) -> dict | list:
        response = requests.post(self._url(path), json=payload, timeout=self.timeout_seconds)
        response.raise_for_status()
        return response.json()

    def put(self, path: str, payload: dict) -> dict | list:
        response = requests.put(self._url(path), json=payload, timeout=self.timeout_seconds)
        response.raise_for_status()
        return response.json()

    def _url(self, path: str) -> str:
        normalized_path = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{normalized_path}"
