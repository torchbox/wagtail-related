from django.db import models


class RelatedSourceField(object):
    def __init__(self, field_name):
        self.field_name = field_name

    def get_field(self, cls):
        return cls._meta.get_field(self.field_name)

    def get_value(self, obj):
        try:
            field = self.get_field(obj.__class__)
            value = field.value_from_object(obj)
            if hasattr(field, 'get_searchable_content'):
                value = field.get_searchable_content(value)

            return value
        except models.fields.FieldDoesNotExist:
            value = getattr(obj, self.field_name, None)
            if hasattr(value, '__call__'):
                value = value()
            return value

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.field_name)
