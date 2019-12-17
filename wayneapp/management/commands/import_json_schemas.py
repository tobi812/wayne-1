import json
from django.core.management import BaseCommand
from wayneapp.services import SchemaLoader, logging
from wayneapp.models import WayneJsonSchema


class Command(BaseCommand):
    help = 'import all json schemas to db'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_loader = SchemaLoader()
        self._logger = logging.getLogger(__name__)

    def handle(self, *args, **kwargs):
        schema_list = self._schema_loader.get_all_json_schemas()

        for schema in schema_list:
            schema_data = json.loads(schema)
            self._create_update_json_schema(schema_data['type'], schema_data['version'], schema_data['data'])

    def _create_update_json_schema(self, type: str, version: str, data: str):
        schema = WayneJsonSchema.objects.filter(type=type, version=version)
        schema_data = {}
        if data != '':
            schema_data = json.loads(data)

        if schema.exists() is False:
            json_schema = WayneJsonSchema()
            json_schema.version = version
            json_schema.type = type
            json_schema.schema = schema_data
            json_schema.save()
        else:
            schema.update(type=type, version=version, schema=schema_data)
