from easybroker_client import EasyBrokerClient

# GitHub Repository:
# https://github.com/EzequielPuerta-TechnicalTests/easybroker/

API_KEY = "l7u502p8v46ba3ppgvj5y2aad50lb9"
client = EasyBrokerClient(api_key=API_KEY)


if __name__ == '__main__':
    try:
        page = 1
        limit = 50
        properties = []

        while page == 1 or len(properties) == limit:
            properties = client.properties.all(params={
                "page": page,
                "limit": limit})
            for property in properties:
                print(property['title'])
            page += 1
    except Exception as error:
        print(str(error))
