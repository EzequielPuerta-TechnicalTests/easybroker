import pytest
from urllib.parse import unquote
from easybroker_client import EasyBrokerClient
from api_resource import Resource


# Fixtures
@pytest.fixture(scope="module")
def auth() -> str:
    yield "l7u502p8v46ba3ppgvj5y2aad50lb9"


@pytest.fixture(scope="module")
def client(auth) -> EasyBrokerClient:
    yield EasyBrokerClient(api_key=auth)


# Model
def test_easybroker_client_creation(auth):
    client = EasyBrokerClient(api_key=auth)
    assert client.headers["accept"] == "application/json"
    assert client.headers["X-Authorization"] == auth


def test_properties_resource(client):
    assert isinstance(client.properties, Resource)


def test_properties_resource_url(client):
    assert client.properties.url == "https://api.stagingeb.com/v1/properties"


# Simple requests
def test_properties_list(client):
    response = client.properties.get()
    assert response.ok
    assert unquote(response.url) == "https://api.stagingeb.com/v1/properties"
    properties = response.json()['content']
    assert len(properties) > 0
    assert properties[0]['property_type']


def test_properties_list_as_json(client):
    properties = client.properties.get(raw=False)
    assert len(properties) > 0
    assert properties[0]['property_type']


def test_properties_all_as_alias_of_get_properties_list_as_json(client):
    properties = client.properties.all()
    assert len(properties) > 0
    assert properties[0]['property_type']


def test_properties_with_query_parameters(client):
    response = client.properties.get(params={
        "page": 1,
        "limit": 5,
    })
    assert response.ok
    assert unquote(response.url) == "https://api.stagingeb.com/v1/properties?page=1&limit=5"
    properties = response.json()['content']
    assert len(properties) == 5
    assert properties[0]['property_type']


def test_properties_with_query_parameters_as_json(client):
    properties = client.properties.get(raw=False, params={
        "page": 1,
        "limit": 5,
    })    
    assert len(properties) == 5
    assert properties[0]['property_type']


def test_properties_with_search_parameters(client):
    response = client.properties.get(params={
        "page": 1,
        "limit": 5,
        "search[property_types][]": "apartment",
        "search[min_price]": 10000,
    })
    assert response.ok
    assert unquote(response.url) == "https://api.stagingeb.com/v1/properties?page=1&limit=5&search[property_types][]=apartment&search[min_price]=10000"
    properties = response.json()['content']
    assert len(properties) > 0
    assert properties[0]['property_type']


def test_properties_with_search_parameters_as_json(client):
    properties = client.properties.get(raw=False, params={
        "page": 1,
        "limit": 5,
        "search[property_types][]": "apartment",
        "search[min_price]": 10000,
    })
    assert len(properties) > 0
    assert properties[0]['property_type']


def test_post_new_property(client):
    property = {
        "status": "published",
        "property_type": "House",
        "title": "Beautiful property in Condesa.",
        "description": "This property is very well-lit in a lovely neighborhood overlooking a park.",
        "location": { "name": "Carmen Serdan, Monterrey, Nuevo León" },
        "operations": [{
            "type": "rental",
            "active": True,
            "currency": "USD",
            "amount": 500000,
        }],
        "show_prices": True,
        "bedrooms": 2,
        "bathrooms": 1,
    }
    response = client.properties.post(json=property)
    assert response.ok
    assert unquote(response.url) == "https://api.stagingeb.com/v1/properties"
    assert response.json()['public_id']


def test_post_new_property_and_get_response_as_json(client):
    property = {
        "status": "published",
        "property_type": "House",
        "title": "Beautiful property in Condesa.",
        "description": "This property is very well-lit in a lovely neighborhood overlooking a park.",
        "location": { "name": "Carmen Serdan, Monterrey, Nuevo León" },
        "operations": [{
            "type": "rental",
            "active": True,
            "currency": "USD",
            "amount": 500000,
        }],
        "show_prices": True,
        "bedrooms": 2,
        "bathrooms": 1,
    }
    new_property = client.properties.post(json=property, raw=False)
    assert new_property['public_id']


def test_retrieve_single_property(client):
    list_response = client.properties.get(params={
        "page": 1,
        "limit": 1,
    })
    first_property = list_response.json()['content'][0]
    response = client.properties.get(first_property['public_id'])
    assert response.ok
    assert (
        unquote(response.url) ==
        f"https://api.stagingeb.com/v1/properties/{first_property['public_id']}"
    )
    property = response.json()
    assert first_property['public_id'] == property['public_id']


def test_retrieve_single_property_as_json(client):
    list_response = client.properties.get(params={
        "page": 1,
        "limit": 1,
    })
    first_property = list_response.json()['content'][0]
    property = client.properties.get(first_property['public_id'], raw=False)
    assert first_property['public_id'] == property['public_id']


def test_find_property_as_alias_of_get_single_property_as_json(client):
    list_response = client.properties.get(params={
        "page": 1,
        "limit": 1,
    })
    first_property = list_response.json()['content'][0]
    property = client.properties.find(first_property['public_id'])
    assert first_property['public_id'] == property['public_id']


# All these resources aren't working with the
# API Key provided, but they are interesting
# to create new features for the client, like
# multilevel resource names and path parameters.
def test_agencies_resource(client):
    assert isinstance(client.partners.agencies, Resource)


def test_agencies_resource_url(client):
    assert client.partners.agencies.url == "https://api.stagingeb.com/v1/integration_partners/agencies"


def test_agencies_resource_with_header_parameters(client):
    response = client.partners.agencies.get(headers={"Country-Code": "AR"})
    assert not response.ok
    assert response.status_code == 401
    assert response.json()['error'] == "Your API key is invalid."


def test_agencies_resource_with_header_parameters_and_get_error(client):
    with pytest.raises(AssertionError) as error:
        client.partners.agencies.get(headers={"Country-Code": "AR"}, raw=False)
    assert str(error.value) == 'Error 401 - Unauthorized | {"error":"Your API key is invalid."}'


def test_properties_from_integration_partners(client):
    request = client.partners.properties.path_param('{property_id}')
    assert request.url == "https://api.stagingeb.com/v1/integration_partners/properties/{property_id}"


def test_property_from_integration_partners(client):
    request = client.partners.properties.path_param('{property_id}').property_integration
    assert request.url == "https://api.stagingeb.com/v1/integration_partners/properties/{property_id}/property_integration"


def test_property_from_integration_partners_with_a_fake_id(client):
    request = client.partners.properties.path_param(42).property_integration
    assert request.url == "https://api.stagingeb.com/v1/integration_partners/properties/42/property_integration"
