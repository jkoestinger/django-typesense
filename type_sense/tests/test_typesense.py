from django.db import models
from django.test import TestCase

from type_sense.models import TypeSenseMixin


class DefaultMockModel(TypeSenseMixin, models.Model):
    class Meta:
        app_label = "mock"


class CustomNameMockModel(TypeSenseMixin, models.Model):
    typesense_schema_name = "custom_name"

    class Meta:
        app_label = "mock"


class CustomFieldsMockModel(TypeSenseMixin, models.Model):
    title = models.TextField()
    price = models.FloatField()

    typesense_fields = [
        {"name": "title", "type": "string"},
        {"name": "custom_price", "type": "float", "attribute": "price"},
    ]

    class Meta:
        app_label = "mock"


class TypeSenseTestCase(TestCase):
    def test_typesense_schema_name_empty(self):
        m = DefaultMockModel()
        self.assertEqual(m.get_typesense_schema_name(), "defaultmockmodel")

    def test_typesense_schema_custom_name(self):
        m = CustomNameMockModel()
        self.assertEqual(m.get_typesense_schema_name(), "custom_name")

    def test_typesense_schema_custom_fields(self):
        m = CustomFieldsMockModel()
        expected = {
            "fields": [
                {"name": "title", "type": "string"},
                {"name": "custom_price", "type": "float"},
            ],
            "name": "customfieldsmockmodel",
        }
        self.assertDictEqual(m._get_schema(), expected)
