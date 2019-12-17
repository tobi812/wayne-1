import json
from django.contrib import admin
from django.utils.safestring import mark_safe

from wayneapp.models import WayneJsonSchema
from wayne import settings


class JsonSchemaAdmin(admin.ModelAdmin):
    fields = ('type', 'version', 'json_schema', 'created', 'modified')
    list_display = ['type', 'version']
    search_fields = ['type', 'version']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def json_schema(self, model):
        json_data = json.dumps(model.schema, sort_keys=True, indent=2)
        return mark_safe('<pre id="json-renderer" class="json-document">' + json_data + '</pre>')

    class Media:
        js = (settings.JSON_VIEWER.get('JS_URL'), settings.WAYNE_ADMIN.get('JS_URL'))
        css = {
            'all': (settings.JSON_VIEWER.get('CSS_URL'), settings.WAYNE_ADMIN.get('CSS_URL'))
        }


admin.site.register(WayneJsonSchema, JsonSchemaAdmin)
