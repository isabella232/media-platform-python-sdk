import json
import unittest

import httpretty

from hamcrest import assert_that, instance_of, is_

from media_platform import FileDescriptor
from media_platform.auth.app_authenticator import AppAuthenticator
from media_platform.http_client.authenticated_http_client import AuthenticatedHTTPClient
from media_platform.job.index_image_job import IndexImageJob
from media_platform.service.file_descriptor import FileType
from media_platform.service.visual_search_service.file_list import FileList
from media_platform.service.rest_result import RestResult
from media_platform.service.source import Source
from media_platform.service.visual_search_service.visual_search_service import VisualSearchService


class TestVisualSearchService(unittest.TestCase):
    authenticator = AppAuthenticator('app', 'secret')
    authenticated_http_client = AuthenticatedHTTPClient(authenticator)

    visual_search_service = VisualSearchService('fish.appspot.com', authenticated_http_client)

    file_path = '/test_file.png'
    test_collection_id = 'collection_id'

    @httpretty.activate
    def test_index_image_request(self):
        self._register_scan_file_request()

        job = (
            self.visual_search_service
                .index_image_request()
                .set_source(Source(self.file_path))
                .set_collection_id(self.test_collection_id)
        ).execute()

        assert_that(job, instance_of(IndexImageJob))
        assert_that(job.status, is_('pending'))
        assert_that(job.serialize()['sources'][0]['path'], is_(self.file_path))

    @httpretty.activate
    def test_find_similar_images_request(self):
        self._register_find_similar_images_request()

        file_list = (
            self.visual_search_service
                .find_similar_images_request()
                .set_image_url('https://upload.wikimedia.org/wikipedia/commons/0/0f/Grosser_Panda.JPG')
                .set_collection_id(self.test_collection_id)
        ).execute()

        assert_that(file_list, instance_of(FileList))
        assert_that(len(file_list.files), is_(3))

        for idx in range(len(file_list.files)):
            assert_that(file_list.files[idx].file_id, is_(f'file-id-{idx}'))

    def _register_scan_file_request(self):
        payload = {
            'type': 'urn:job:visual-search.index-image',
            'id': 'g_1',
            'groupId': None,
            'status': 'pending',
            'issuer': 'urn:app:app-id',
            'sources': [
                {'path': self.file_path}
            ],
            'specification': {},
            'callback': {},
            'dateUpdated': '2017-05-22T07:17:44Z',
            'dateCreated': '2017-05-22T07:17:44Z'
        }
        response = RestResult(0, 'OK', payload)
        httpretty.register_uri(
            httpretty.POST,
            f'https://fish.appspot.com/_api/visual_search/collections/{self.test_collection_id}/index',
            json.dumps(response.serialize())
        )

    def _register_find_similar_images_request(self):
        payload = [
            FileDescriptor('/fish.png', 'file-id-0', FileType.file, 'image/png', 123).serialize(),
            FileDescriptor('/cat.png', 'file-id-1', FileType.file, 'image/png', 123).serialize(),
            FileDescriptor('/dog.png', 'file-id-2', FileType.file, 'image/png', 123).serialize(),
        ]
        response = RestResult(0, 'OK', payload)
        httpretty.register_uri(
            httpretty.POST,
            f'https://fish.appspot.com/_api/visual_search/collections/{self.test_collection_id}/search',
            json.dumps(response.serialize())
        )
