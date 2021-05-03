from copy import deepcopy

from django.db import models

from type_sense.client import client


class TypeSenseMixin(models.Model):

    typesense_fields = []
    typesense_schema_name = None
    typesense_default_sorting_field = None

    def get_typesense_schema_name(self) -> str:
        if self.typesense_schema_name:
            return self.typesense_schema_name
        return self.__class__.__name__.lower()

    def get_typesense_fields(self):
        fields = deepcopy(self.typesense_fields)

        # Auto adds the pk as Id if absent
        if not any(field["name"] == "id" for field in fields):
            fields.append({"name": "id", "type": "string", "attribute": "pk"})

        return fields

    def _get_typesense_schema(self):
        schema = {
            "name": self.get_typesense_schema_name(),
            "fields": deepcopy(self.typesense_fields),
        }

        if self.typesense_default_sorting_field:
            schema["default_sorting_field"] = self.typesense_default_sorting_field

        existing_fields = []

        for field in schema["fields"]:
            existing_fields.append(field["name"])
            if "attribute" in field:
                del field["attribute"]

        return schema

    def _get_typesense_field_value(self, field):
        if "attribute" in field:
            attribute = field["attribute"]
        else:
            attribute = field["name"]
        return getattr(self, attribute)

    def create_typesense_collection(self):
        client.collections.create(self._get_typesense_schema())

    def drop_typesense_collection(self):
        client.collections[self.get_typesense_schema_name()].delete()

    def retrieve_typesense_collection(self):
        return client.collections[self.get_typesense_schema_name()].retrieve()

    def upsert_typesense_document(self):
        fields = {}

        for field in self.get_typesense_fields():
            fields[field["name"]] = self._get_typesense_field_value(field)

        return fields

    def delete_typesense_document(self):
        client.collections[self.get_typesense_schema_name()].documents[
            str(self.pk)
        ].delete()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.upsert_typesense_document()

    def delete(self, **kwargs):
        self.delete_typesense_document()
        super().delete(**kwargs)

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        return errors

    class Meta:
        abstract = True
