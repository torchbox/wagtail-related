from collections import OrderedDict

from django.core.exceptions import ImproperlyConfigured

from taggit.models import Tag, TaggedItemBase
from wagtail.core.models import Page
from wagtail.search.backends import get_search_backend
from wagtail.search.backends.elasticsearch5 import Elasticsearch5SearchBackend
from wagtail.search.index import Indexed

from wagtailrelated.backends.base import BaseRelatedBackend


class InvalidSearchBackendError(ImproperlyConfigured):
    pass


class Elasticsearch5RelatedBackend(BaseRelatedBackend):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        wagtailsearch_backend = self.params.get('wagtailsearch_backend', 'default')
        search_backend = get_search_backend(backend=wagtailsearch_backend)
        if not isinstance(search_backend, Elasticsearch5SearchBackend):
            raise InvalidSearchBackendError(
                'Elasticsearch5RelatedBackend was configured to use '
                'WAGTAILSEARCH_BACKENDS[\'{}\'] which is not '
                'wagtail.search.backends.elasticsearch5 backend'.format(wagtailsearch_backend)
            )

        self.search_backend = search_backend
        self.min_term_freq = self.params.get('min_term_freq', 1)
        self.min_doc_freq = self.params.get('min_doc_freq', 1)

    def get_tags(self, obj):
        if not isinstance(obj, Indexed):
            return []

        results = self.get_similar_items(obj)
        tags = self._extract_tags(results)
        return tags

    def get_similar_items(self, obj, **kwargs):
        obj = obj.specific
        model = obj.specific_class

        limit = kwargs.get('limit', 20)
        content_types = kwargs.get('content_types')
        exclude_pks = kwargs.get('exclude_pks')

        params = dict(
            index=self.search_backend.get_index_for_model(model).name,
            body=self._get_query(obj, content_types, exclude_pks),
            _source=False,
            from_=0,
            size=limit,
            stored_fields='pk'
        )

        hits = self.search_backend.es.search(**params)

        # Get pks and scores from results
        pks = []
        scores = {}
        for hit in hits['hits']['hits']:
            pk = int(hit['fields']['pk'][0])
            pks.append(pk)
            scores[pk] = hit['_score']

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
                result_obj = results_dict[pk]
            except KeyError:
                # Just ignore, if there is no obj with this pk
                continue

            result_obj._score = scores[pk]
            yield result_obj

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

    def _get_query(self, obj, content_types, exclude_pks):
        model = obj.specific_class
        model_index = self.search_backend.get_index_for_model(model)
        model_mapping = model_index.mapping_class(model)

        query = {
            'query': {
                'bool': {
                    'must': [
                        self._get_more_like_this_query(obj, model_mapping),
                        self._get_filter_query(model_index, content_types, exclude_pks),
                    ]
                }
            }
        }

        return query

    def _get_filter_query(self, model_index, content_types, exclude_pks):
        query = {}

        if content_types:
            content_type_strings = [
                model_index.mapping_class(model).get_content_type()
                for model in content_types
            ]
            query.update({
                'must': {
                    'terms': {
                        'content_type': content_type_strings,
                    }
                }
            })

        if exclude_pks:
            query.update({
                'must_not': {
                    'terms': {
                        'pk': exclude_pks,
                    }
                }
            })

        return {'bool': query} if len(query) > 0 else {}

    def _get_more_like_this_query(self, obj, model_mapping):
        query = {
            'more_like_this': {
                'like': [
                    {
                        '_type': model_mapping.get_document_type(),
                        '_id': model_mapping.get_document_id(obj),
                    }
                ],
                'min_term_freq': self.min_term_freq,
                'min_doc_freq': self.min_doc_freq
            }
        }

        return query


# Shortcut
RelatedBackend = Elasticsearch5RelatedBackend
