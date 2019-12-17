from django.db import models
from django.contrib.postgres.fields import JSONField
from model_utils.models import TimeStampedModel


class JsonSchema(TimeStampedModel):
    type = models.TextField(null=False)
    version = models.TextField(null=False)
    schema = JSONField(null=False)
