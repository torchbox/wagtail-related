from django.db.models import Q
from taggit.models import TaggedItemBase, Tag
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.backends import get_search_backend
from wagtail.wagtailsearch.index import Indexed

from wagtailautotagging.backends.base import BaseAutotaggingBackend


class Elasticsearch5AutotaggingBackend(BaseAutotaggingBackend):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        # TODO: Add check that wagtailsearch_backend is Elasticsearch5SearchBackend
        wagtailsearch_backend = self.params.get('wagtailsearch_backend', 'default')
        self.search_backend = get_search_backend(backend=wagtailsearch_backend)

    def get_tags(self, page):
        if not isinstance(page, Indexed):
            return []

        results = self._get_similar_pages(page)
        tags = self._extract_tags(results)
        return tags

    def _extract_tags(self, results):
        tag_filter = Q()
        for page in results:
            if not page:
                continue

            for field in page._meta.get_fields():
                if field.is_relation and issubclass(field.related_model, TaggedItemBase):
                    pages_field = getattr(page, field.name)
                    tag_filter |= Q(pk__in=pages_field.values_list('tag_id'))

        if not tag_filter:
            return []

        # TODO: Add weights for each tag (based on count?)
        tags = Tag.objects.filter(tag_filter).distinct()
        tags = [tag.name for tag in tags]

        return tags

    def _get_similar_pages(self, page):
        model = page.__class__

        params = dict(
            index=self.search_backend.get_index_for_model(model).name,
            body=self._get_query(page),
            _source=False,
            from_=0,
            stored_fields='pk'
        )

        hits = self.search_backend.es.search(**params)

        # Get pks from results
        pks = [hit['fields']['pk'][0] for hit in hits['hits']['hits']]

        # Find objects in database and add them to dict
        # Queryset must contain specific objects. Otherwise we would not be able
        # to get tags from models
        queryset = Page.objects.filter(pk__in=pks).specific()
        results = dict((str(obj.pk), obj) for obj in queryset)

        # Return results in order given by Elasticsearch
        return [results.get(str(pk), None) for pk in pks if results[str(pk)]]

    def _get_query(self, page):
        mapping = self.search_backend.mapping_class(page.__class__)
        doc_type = mapping.get_document_type()
        document_id = mapping.get_document_id(page)

        existing_doc_ref = {
            '_type': doc_type,
            '_id': document_id,
        }

        query = {
            "query": {
                "more_like_this": {
                    # It's possible to specify fields to search, so we can use autotagging_source_fields,
                    # but by default elasticsearch uses all string fields to find similar documents.
                    # TODO: Decide if we need to use autotagging_source_fields here.
                    "like": [
                        existing_doc_ref
                    ],
                    # TODO: Decided if we need this to be configurable
                    "min_term_freq": 1,
                    "min_doc_freq": 1
                }
            }
        }

        return query


# Shortcut
AutotaggingBackend = Elasticsearch5AutotaggingBackend
