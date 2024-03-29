from django.test import TestCase
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APIClient

from wayneapp.controllers import DeleteBusinessEntityController
from wayneapp.services import BusinessEntityManager, settings


class TestDeleteBusinessEntityController(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestDeleteBusinessEntityController, cls).setUpClass()
        settings.SCHEMA_PACKAGE_NAME = 'wayneapp.tests.test_schema'

    @patch.object(BusinessEntityManager, 'delete', return_value=1)
    @patch.object(DeleteBusinessEntityController, 'has_delete_permission', return_value=True)
    def test_delete_business_entity_should_work(self, mock_manager, mock_controller):
        data = {
            'version': 'v1',
            'key': 'x-id',
        }

        client = APIClient()
        client.force_authenticate(user=None)
        response = client.post('/api/test_entity/delete', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(BusinessEntityManager, 'delete', side_effect=Exception('Test'))
    @patch.object(DeleteBusinessEntityController, 'has_delete_permission', return_value=True)
    def test_delete_business_entity_should_fail(self, mock_manager, mock_controller):
        data = {
            'version': 'v1',
            'key': 'x-id',
        }

        with self.assertRaises(Exception):
            client = APIClient()
            client.force_authenticate(user=None)
            response = client.post('/api/test_entity/delete', data, format='json')

            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch.object(BusinessEntityManager, 'delete', side_effect=Exception('Test'))
    @patch.object(DeleteBusinessEntityController, 'has_delete_permission', return_value=False)
    def test_delete_business_entity_should_fail_unauthorized(self, mock_manager, mock_controller):
        data = {
            'version': 'v1',
            'key': 'x-id',
        }

        client = APIClient()
        client.force_authenticate(user=None)
        response = client.post('/api/test_entity/delete', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'message': 'unauthorized'})

    @patch.object(BusinessEntityManager, 'delete_by_key', return_value=2)
    @patch.object(DeleteBusinessEntityController, 'has_delete_permission', return_value=True)
    def test_delete_business_entity_all_versions_success(self, mock_manager, mock_controller):
        data = {
            'key': 'x-id',
        }

        client = APIClient()
        client.force_authenticate(user=None)
        response = client.post('/api/test_entity/delete', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'entity with key x-id deleted from all versions'})

    @patch.object(BusinessEntityManager, 'delete_by_key', return_value=0)
    @patch.object(DeleteBusinessEntityController, 'has_delete_permission', return_value=True)
    def test_delete_business_entity_all_versions_fail(self, mock_manager, mock_controller):
        data = {
            'key': 'x-id',
        }

        client = APIClient()
        client.force_authenticate(user=None)
        response = client.post('/api/test_entity/delete', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'entity with key x-id not found'})

    @patch.object(BusinessEntityManager, 'delete_by_key', return_value=2)
    @patch.object(DeleteBusinessEntityController, 'has_delete_permission', return_value=False)
    def test_delete_business_entity_all_versions_fail_unauthorized(self, mock_manager, mock_controller):
        data = {
            'key': 'x-id',
        }

        client = APIClient()
        client.force_authenticate(user=None)
        response = client.post('/api/test_entity/delete', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'message': 'unauthorized'})
