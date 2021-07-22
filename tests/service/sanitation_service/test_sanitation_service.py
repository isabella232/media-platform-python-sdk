import json
import unittest

import httpretty
from hamcrest import assert_that, instance_of, is_, contains_string, starts_with

from media_platform.auth.app_authenticator import AppAuthenticator
from media_platform.http_client.authenticated_http_client import AuthenticatedHTTPClient
from media_platform.service.destination import Destination
from media_platform.service.file_descriptor import FileDescriptor, FileType
from media_platform.service.sanitation_service.sanitation_service import SanitationService
from media_platform.service.sanitation_service.sanitation_response import SanitationResponse, \
    SanitationResult, SanitationParams
from media_platform.service.rest_result import RestResult
from media_platform.service.source import Source


class TestSanitationService(unittest.TestCase):
    authenticator = AppAuthenticator('app', 'secret')
    authenticated_http_client = AuthenticatedHTTPClient(authenticator)

    sanitation_service = SanitationService('fish.barrel', authenticated_http_client)

    @httpretty.activate
    def test_sanitation_request(self):
        payload = SanitationResponse(
            FileDescriptor('/result.svg', 'file-id', FileType.file, 'image/svg+xml', 123),
            SanitationResult(True, SanitationParams(True, []))
        ).serialize()
        response_body = RestResult(0, 'OK', payload)
        httpretty.register_uri(
            httpretty.POST,
            'https://fish.barrel/_api/security/sanitize',
            body=json.dumps(response_body.serialize())
        )

        response = self.sanitation_service.sanitation_request().\
            set_source(Source('/test.svg')).set_destination(Destination('/result.svg')).execute()

        assert_that(response.serialize(), is_(payload))
        assert_that(response.file_descriptor, instance_of(FileDescriptor))
        assert_that(response.sanitation_result, instance_of(SanitationResult))
        assert_that(response.sanitation_result.sanitation_params, instance_of(SanitationParams))
