import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.exceptions import RetryError
from requests.structures import CaseInsensitiveDict
from requests_toolbelt import MultipartEncoder
from typing import Type

from media_platform.lang.serialization import Deserializable
from media_platform.auth.app_authenticator import AppAuthenticator
from media_platform.exception.media_platform_exception import MediaPlatformException
from media_platform.http.response_processor import ResponseProcessor


class AuthenticatedHTTPClient(object):
    USER_AGENT = 'WixMP Python SDK 1.x'
    APPLICATION_JSON = 'application/json'
    RETRYABLE_CODES = [500, 503, 504, 429]
    RETRYABLE_METHODS = ['GET', 'POST', 'PUT', 'DELETE']

    def __init__(self, app_authenticator, retry_count=5, retry_backoff_factor=0.2):
        # type: (AppAuthenticator, int, float) -> None

        self._app_authenticator = app_authenticator
        self._session = requests.Session()

        retry = urllib3.Retry(total=retry_count, backoff_factor=retry_backoff_factor,
                              status_forcelist=self.RETRYABLE_CODES, method_whitelist=self.RETRYABLE_METHODS)

        self._session.mount('http://', HTTPAdapter(max_retries=retry))
        self._session.mount('https://', HTTPAdapter(max_retries=retry))

    def get(self, url, params=None, payload_type=None):
        # type: (str, dict, Type[Deserializable]) -> Deserializable or None

        return self._send_request('GET', url, params=params, payload_type=payload_type)

    def post(self, url, data=None, payload_type=None):
        # type: (str, dict, Type[Deserializable]) -> object or None

        return self._send_request('POST', url, json=data, payload_type=payload_type)

    def post_data(self, url, content, mime_type, params=None, payload_type=None):
        # type: (str, str, str, dict, Type[Deserializable]) -> Deserializable or None

        fields = {
            'file': ('file-name', content, mime_type)
        }
        fields.update(params)

        encoder = MultipartEncoder(fields)

        try:
            response = self._session.post(url, data=encoder, headers={'Content-Type': encoder.content_type})
        except RetryError as e:
            raise MediaPlatformException(e)

        return ResponseProcessor.process(response, payload_type)

    # todo: delete

    def _send_request(self, verb, url, json=None, params=None, payload_type=None):
        # type: (str, str, dict, dict, Type[Deserializable]) -> object or None

        try:
            response = self._session.request(verb, url, params=params, json=json, headers=self._headers())
        except RetryError as e:
            raise MediaPlatformException(e)

        return ResponseProcessor.process(response, payload_type)

    def _headers(self):
        # type: () -> CaseInsensitiveDict

        signed_token = self._app_authenticator.default_signed_token()

        headers = requests.utils.default_headers()
        headers['Authorization'] = signed_token
        headers['User-Agent'] = self.USER_AGENT
        headers['Accept'] = self.APPLICATION_JSON

        return headers
