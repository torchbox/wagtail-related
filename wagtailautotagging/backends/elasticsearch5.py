from collections import OrderedDict

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

    def get_tags(self, obj):
        if not isinstance(obj, Indexed):
            return []

        results = self._get_similar_items(obj)
        tags = self._extract_tags(results)
        return tags

    def _extract_tags(self, results):
        tag_pks = []
        tag_counts = {}

        for result_obj in results:
            for field in result_obj._meta.get_fields():
                if field.is_relation and issubclass(field.related_model, TaggedItemBase):
                    field = getattr(result_obj, field.name)
                    obj_tag_pks = list(field.values_list('tag_id', flat=True))
                    tag_pks += obj_tag_pks
                    for obj_tag_pk in obj_tag_pks:
                        tag_counts[obj_tag_pk] = tag_counts.get(obj_tag_pk, 0) + 1

        if not tag_pks:
            return []

        tag_counts = OrderedDict(sorted(tag_counts.items(), key=lambda i: i[1], reverse=True))

        results_dict = Tag.objects.in_bulk(tag_pks)
        tag_names = []
        for tag_pk in tag_counts.keys():
            try:
                tag_names.append(results_dict[tag_pk].name)
            except KeyError:
                # Just ignore, if there is not obj with this pk
                pass

        return tag_names

    def _get_similar_items(self, obj):
        model = obj.__class__

        params = dict(
            index=self.search_backend.get_index_for_model(model).name,
            body=self._get_query(obj),
            _source=False,
            from_=0,
            stored_fields='pk'
        )

        hits = self.search_backend.es.search(**params)

        # Get pks from results
        pks = [int(hit['fields']['pk'][0]) for hit in hits['hits']['hits']]

        if isinstance(obj, Page):
            # If we work with pages, `queryset` must contain specific objects.
            # Otherwise we would not be able to get tags from models
            queryset = Page.objects.specific()
        else:
            queryset = model.objects.all()

        results_dict = queryset.in_bulk(pks)

        # Return results in order given by Elasticsearch
        for pk in pks:
            try:
                yield results_dict[pk]
            except KeyError:
                # Just ignore, if there is not obj with this pk
                pass

    def _get_query(self, obj):
        mapping = self.search_backend.mapping_class(obj.__class__)
        doc_type = mapping.get_document_type()
        document_id = mapping.get_document_id(obj)

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
