from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

__version__ = '0.1.0'

default_app_config = 'wagtailrelated.apps.WagtailRelatedAppConfig'


class InvalidBackendError(ImproperlyConfigured):
    pass


def get_backend_config():
    backends = getattr(settings, 'WAGTAIL_RELATED_BACKENDS', {})

    return backends


def import_backend(dotted_path):
    backend_module = import_module(dotted_path)
    return backend_module.RelatedBackend


def get_backend(backend='default', **kwargs):
    backends = get_backend_config()

    # Try to find the backend
    conf = backends[backend]

    # Backend is a conf entry
    params = conf.copy()
    params.update(kwargs)
    backend = params.pop('BACKEND')

    # Try to import the backend
    try:
        backend_cls = import_backend(backend)
    except ImportError as e:
        raise InvalidBackendError("Could not find backend '%s': %s" % (
            backend, e))

    # Create backend
    return backend_cls(params)
