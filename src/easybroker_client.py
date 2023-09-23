from wrapped_resource import WrappedResource
from api_resource import Resource
from parent_resource import ParentResource


# Root resources
contact_requests: Resource = WrappedResource("contact_requests")
properties: Resource = WrappedResource("properties")
mls_properties: Resource = WrappedResource("mls_properties")
locations: Resource = WrappedResource("locations")
listing_statuses: Resource = WrappedResource("listing_statuses")
contacts: Resource = WrappedResource("contacts")
collaborations: Resource = WrappedResource("collaborations")

# Sub resource for integration partners's properties resource
property_integration: Resource = WrappedResource("property_integration")

# Integration partners resources
agencies: Resource = WrappedResource("agencies")
agents: Resource = WrappedResource("agents")
partners_contact_requests: Resource = WrappedResource("contact_requests")
partners_listing_statuses: Resource = WrappedResource("listing_statuses")
partners_properties: Resource = WrappedResource(
    "properties",
    subs=[property_integration])
integration_partners: Resource = WrappedResource(
    "integration_partners",
    subs=[
        agencies,
        agents,
        partners_contact_requests,
        partners_listing_statuses,
        partners_properties])


# API Client
class EasyBrokerClient(ParentResource):
    def __init__(self, api_key: str) -> None:
        super().__init__({
            "accept": "application/json",
            "X-Authorization": api_key,
        })

    contact_requests: Resource = contact_requests
    properties: Resource = properties
    mls_properties: Resource = mls_properties
    locations: Resource = locations
    listing_statuses: Resource = listing_statuses
    contacts: Resource = contacts
    collaborations: Resource = collaborations
    partners: Resource = integration_partners
