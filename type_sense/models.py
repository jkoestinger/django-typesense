from copy import deepcopy

from django.db import models

from type_sense.client import client


class TypeSenseMixin(models.Model):

    typesense_fields = []
    typesense_schema_name = None

    def get_typesense_schema_name(self) -> str:
        if self.typesense_schema_name:
            return self.typesense_schema_name
        return self.__class__.__name__.lower()

    def _get_schema(self):
        schema = {
            "name": self.get_typesense_schema_name(),
            "fields": deepcopy(self.typesense_fields),
        }

        for field in schema["fields"]:
            if "attribute" in field:
                del field["attribute"]

        return schema

    def create_collection(self):
        client.collections.create(self._get_schema())

    def drop_collection(self):
        client.collections[self.get_typesense_schema_name()].delete()

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        return errors

    class Meta:
        abstract = True
