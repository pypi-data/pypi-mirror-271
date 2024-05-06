import requests
from requests.exceptions import ConnectionError, MissingSchema


class APIConnection:
    def __init__(self, url) -> None:
        self._url = url

    def get(self, endpoint) -> dict[str, str]:
        full_url = f'{self._url}{endpoint}'
        return self.request('GET', full_url).json()

    def request(self, http_verb, full_url):
        try:
            if http_verb == 'GET':
                return requests.get(full_url)
        except MissingSchema:
            raise MissingSchema(
                'Error while trying to connect to third party api. Probably and invalid URL.'
            )
        except ConnectionError:
            raise ConnectionError(
                'Error while trying to connect to third party api.'
            )
