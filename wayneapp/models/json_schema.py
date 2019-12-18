from django.db import models
from django.contrib.postgres.fields import JSONField
from model_utils.models import TimeStampedModel
from wayne import settings


class JsonSchemaApp(TimeStampedModel):
    business_entity = models.TextField(null=False)
    version = models.TextField(null=False)
    schema = JSONField(null=False)

    class Meta:
        app_label = settings.SCHEMA_APP_LABEL
