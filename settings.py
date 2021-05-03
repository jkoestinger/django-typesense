from django.conf import settings

if hasattr(settings, "TYPESENSE"):
    TYPESENSE = settings.TYPESENSE
else:
    TYPESENSE = {"nodes": [{"host": "localhost", "port": "8108", "protocol": "http"}]}
