from wrapped_resource import WrappedResource
from api_resource import Resource
from parent_resource import ParentResource


# Resources
properties = WrappedResource("properties")

agencies = WrappedResource("agencies")

property_integration = WrappedResource("property_integration")

properties_integration = WrappedResource(
    "properties",
    subs=[property_integration])

integration_partners = WrappedResource(
    "integration_partners",
    subs=[
        agencies,
        properties_integration])


# API Client
class EasyBrokerClient(ParentResource):
    def __init__(self, api_key: str) -> None:
        super().__init__({
            "accept": "application/json",
            "X-Authorization": api_key,
        })

    properties: Resource = properties
    partners: Resource = integration_partners
