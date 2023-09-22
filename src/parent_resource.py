from wrapped_resource import WrappedResource
from api_resource import Resource


class ParentResource:
    __BASE_URL: str = "https://api.stagingeb.com/v1"

    @property
    def url(self) -> str:
        return self.__BASE_URL

    def __init__(self, headers: dict[str]) -> None:
        self.headers: dict[str] = headers

    def _resource(
        self,
        *path: str,
        subs: list[WrappedResource],
    ) -> Resource:
        if subs:
            superclasses = (Resource, ParentResource)
        else:
            superclasses = (Resource,)

        dynamic_resource_class = type(path[-1], superclasses, {})
        dynamic_resource = dynamic_resource_class(self.headers, self.url, *path)
        for wrapped_resource in subs:
            setattr(
                dynamic_resource_class,
                wrapped_resource.accessor,
                wrapped_resource)
        return dynamic_resource
