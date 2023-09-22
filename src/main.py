from easybroker_client import EasyBrokerClient


API_KEY = "l7u502p8v46ba3ppgvj5y2aad50lb9"
client = EasyBrokerClient(api_key=API_KEY)


if __name__ == '__main__':
    try:
        page = 1
        limit = 50
        first_request = True

        while first_request or len(properties) == limit:
            properties = client.properties.all(params={
                "page": page,
                "limit": limit})
            for property in properties:
                print(property['title'])
            if first_request:
                first_request = False
            page += 1
    except Exception as error:
        print(str(error))