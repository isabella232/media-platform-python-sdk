import json
import unittest

import httpretty

from hamcrest import assert_that, instance_of, is_

from media_platform import FileDescriptor
from media_platform.auth.app_authenticator import AppAuthenticator
from media_platform.http_client.authenticated_http_client import AuthenticatedHTTPClient
from media_platform.job.index_image_job import IndexImageJob, IndexImageSpecification
from media_platform.service.file_descriptor import FileType
from media_platform.service.visual_search_service.collection import Collection
from media_platform.service.visual_search_service.file_list import FileList
from media_platform.service.rest_result import RestResult
from media_platform.service.source import Source
from media_platform.service.visual_search_service.model import Model
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
                .set_specification(IndexImageSpecification(self.test_collection_id))
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

    @httpretty.activate
    def test_create_model_request(self):
        self._register_create_model_request()

        model = (
            self.visual_search_service
                .create_model_request()
                .set_model_id('test-model-id')
                .set_name('test-model-name')
                .set_description('test-model-description')
        ).execute()

        assert_that(model, instance_of(Model))
        assert_that(model.model_id, is_('test-model-id'))

    @httpretty.activate
    def test_create_collection_request(self):
        self._register_create_collection_request()

        collection = (
            self.visual_search_service
                .create_collection_request()
                .set_collection_id('test-collection-id')
                .set_name('test-collection-name')
                .set_project_id('test-project-id')
                .set_model_id('test-model-id')
        ).execute()

        assert_that(collection, instance_of(Collection))
        assert_that(collection.collection_id, is_('test-collection-id'))
        assert_that(collection.model_id, is_('test-model-id'))

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

    def _register_create_model_request(self):
        payload = {
            "id": "test-model-id",
            "name": "test-model-name",
            "description": "test-model-description"
        }
        response = RestResult(0, 'OK', payload)
        httpretty.register_uri(
            httpretty.POST,
            f'https://fish.appspot.com/_api/visual_search/models',
            json.dumps(response.serialize())
        )

    def _register_create_collection_request(self):
        payload = {
            "id": "test-collection-id",
            "name": "test-collection-name",
            "projectId": "test-project-id",
            "modelId": "test-model-id"
        }
        response = RestResult(0, 'OK', payload)
        httpretty.register_uri(
            httpretty.POST,
            f'https://fish.appspot.com/_api/visual_search/collections',
            json.dumps(response.serialize())
        )
