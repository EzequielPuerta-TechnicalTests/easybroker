import pytest
from urllib.parse import unquote
from easybroker_client import EasyBrokerClient, EasyBrokerResource


@pytest.fixture(scope="module")
def auth() -> str:
    yield "l7u502p8v46ba3ppgvj5y2aad50lb9"


@pytest.fixture(scope="module")
def client(auth) -> EasyBrokerClient:
    yield EasyBrokerClient(api_key=auth)


def test_easybroker_client_creation(auth):
    client = EasyBrokerClient(api_key=auth)
    assert client.api_key == auth


def test_properties_resource(client):
    assert isinstance(client.properties, EasyBrokerResource)


def test_properties_resource_url(client):
    assert client.properties.url == "https://api.stagingeb.com/v1/properties"


def test_properties_list(client):
    response = client.properties.get()
    assert response.ok
    assert unquote(response.url) == "https://api.stagingeb.com/v1/properties"
    properties = response.json()['content']
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


def test_properties_with_search_parameters(client):
    response = client.properties.get(params={
        "page": 1,
        "limit": 5,
        "search[property_types][]": "apartment",
        "search[min_price]": 10000,
    })
    assert response.ok
    assert unquote(response.url) == "https://api.stagingeb.com/v1/properties?page=1&limit=5&search[property_types][]=apartment&search[min_price]=10000"


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


def test_retrieve_property(client):
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


def test_agencies_resource(client):
    assert isinstance(client.agencies, EasyBrokerResource)


def test_agencies_resource_url(client):
    assert client.agencies.url == "https://api.stagingeb.com/v1/integration_partners/agencies"
