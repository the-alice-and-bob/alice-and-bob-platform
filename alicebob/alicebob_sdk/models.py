from django.db import models
from uuid_extensions import uuid7


class UUID7Field(models.UUIDField):
    def __init__(self, *args, **kwargs):
        # Set default to uuid7 if no default is provided
        kwargs['default'] = kwargs.get('default', lambda: uuid7())
        super().__init__(*args, **kwargs)


__all__ = ('UUID7Field',)
