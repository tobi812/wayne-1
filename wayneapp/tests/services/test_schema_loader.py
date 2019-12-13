from django.test import TestCase
from unittest.mock import patch
from wayneapp.services import settings

import pkgutil

from wayneapp.services import SchemaLoader


class TestSchemaLoader(TestCase):

    def setUp(self):
        self._schema_loader = SchemaLoader()
        self._business_entity = 'test_entity'
        self._version_1 = 'v1'
        self._version_latest = 'v2'

    @classmethod
    def setUpClass(cls):
        super(TestSchemaLoader, cls).setUpClass()
        settings.SCHEMA_PACKAGE_NAME = 'wayneapp.tests.test_schema'

    @patch.object(pkgutil, 'get_data', return_value=None)
    def test_load_empty_schema(self, mock_pkgutil):
        get_json = self._schema_loader.load('test_entity', 'v1')

        self.assertEqual('{}', get_json)

    def test_load_non_existing_schema(self):
        with self.assertRaises(FileNotFoundError):
            self._schema_loader.load(self._business_entity, 'WRONG_VERSION')

        with self.assertRaises(FileNotFoundError):
            self._schema_loader.load('WRONG_ENTITY', self._version_1)

    def test_load_json_success(self):
        get_json_schema = self._schema_loader.load(self._business_entity, self._version_1)
        test_json_schema = pkgutil.get_data(settings.SCHEMA_PACKAGE_NAME, self._business_entity + '/' +
                                            self._business_entity + '_' + self._version_1 + '.json')

        self.assertEqual(test_json_schema.decode('utf-8'), get_json_schema)

    def test_get_all_versions(self):
        schema_all_versions = self._schema_loader.get_all_versions(self._business_entity)

        self.assertEqual({self._version_1, self._version_latest}, schema_all_versions)

    def test_get_schema_latest_version(self):
        schema_latest_version = self._schema_loader.get_schema_latest_version(self._business_entity)

        self.assertEqual(self._version_latest, schema_latest_version)
