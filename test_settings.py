INSTALLED_APPS = ("type_sense",)
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
SECRET_KEY = "testing-secret-key"

TYPESENSE = {
    "nodes": [{"host": "localhost", "port": "8108", "protocol": "http"}],
    "api_key": "test-key",
}
