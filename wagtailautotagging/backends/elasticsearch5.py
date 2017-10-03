from wagtail.wagtailsearch.backends import get_search_backend

from wagtailautotagging.backends.base import BaseAutotaggingBackend


class Elasticsearch5AutotaggingBackend(BaseAutotaggingBackend):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        # TODO: Add check that wagtailsearch_backend is Elasticsearch5SearchBackend
        wagtailsearch_backend = self.params.get('wagtailsearch_backend', 'default')
        self.backend = get_search_backend(backend=wagtailsearch_backend)

    def get_tags(self, page):
        return []


# Shortcut
AutotaggingBackend = Elasticsearch5AutotaggingBackend
