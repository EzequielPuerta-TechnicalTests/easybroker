import requests


class EasyBrokerResource:
    __BASE_URL: str = "https://api.stagingeb.com/v1"

    def __init__(self, api_key: str, *path: str) -> None:
        self.headers: str = {
            "accept": "application/json",
            "X-Authorization": api_key,
        }
        self.path: tuple[str] = path
        
    @property
    def url(self) -> str:
        return "/".join((self.__BASE_URL, *self.path))
    
    def get(self, _id: str | None = None, params: dict | None = None):
        if _id:
            self.path_param(_id)
        return requests.get(self.url, params=params, headers=self.headers)
    
    def post(self, params: dict | None = None, json: dict | None = None):
        self.headers.update({"content-type": "application/json"})
        return requests.post(
            self.url,
            params=params,
            json=json,
            headers=self.headers)
    
    def path_param(self, value: str):
        self.path = (*self.path, value)
        return self


class IntegrationPartnersResource(EasyBrokerResource):
    __URL: str = "integration_partners"

    def __init__(self, api_key: str, *path: str) -> None:
        super().__init__(api_key, self.__URL, *path)

class EasyBrokerClient:
    __resource = EasyBrokerResource
    __partners = IntegrationPartnersResource

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key

    @property
    def properties(self):
        return self.__resource(self.api_key, "properties")
    
    @property
    def agencies(self):
        return self.__partners(self.api_key, "agencies")
