import requests
from typing import Any


class Resource:
    def __init__(self, headers: dict[str], *path: str) -> None:
        self.headers: dict[str] = headers
        self.path: tuple[str] = path

    @property
    def url(self) -> str:
        return "/".join((*self.path,))

    def add_path_param(self, value: Any):
        self.path = (*self.path, str(value))
        return self

    def _request(self, method: str, **kwargs):
        try:
            self.headers.update(kwargs["headers"])
        except TypeError:
            pass
        finally:
            kwargs["headers"] = self.headers
        return requests.request(method, self.url, **kwargs)

    def get(self,
            _id: str | None = None,
            params: dict | None = None,
            headers: dict | None = None,
            raw: bool = True,
    ):
        if _id:
            self.add_path_param(_id)
        response = self._request("get", params=params, headers=headers)
        if raw:
            return response
        elif not raw and response.ok:
            as_json = response.json()
            return as_json["content"] if not _id else as_json
        else:
            raise AssertionError(f"Error {response.status_code} - {response.reason} | {response.text}")

    def post(self,
             params: dict | None = None,
             json: dict | None = None,
             headers: dict | None = None,
             raw: bool = True,
    ):
        self.headers.update({"content-type": "application/json"})
        response = self._request("post", params=params, json=json, headers=headers)
        if raw:
            return response
        elif not raw and response.ok:
            return response.json()
        else:
            raise AssertionError(f"Error {response.status_code} - {response.reason} | {response.text}")

    def patch(self,
              json: dict | None = None,
              headers: dict | None = None,
    ):
        return self._request("patch", json=json, headers=headers)

    def find(self,
            _id: str,
            params: dict | None = None,
            headers: dict | None = None,
    ):
        return self.get(_id=_id, params=params, headers=headers, raw=False)

    def all(self,
            params: dict | None = None,
            headers: dict | None = None,
    ):
        return self.get(params=params, headers=headers, raw=False)