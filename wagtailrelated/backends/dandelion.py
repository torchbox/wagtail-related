from collections import OrderedDict

import requests
from django.utils.text import Truncator

from wagtailrelated.backends.base import BaseRelatedBackend
from wagtailrelated.utils import extract_text


class DandelionRelatedBackend(BaseRelatedBackend):
    entity_extraction_api = 'https://api.dandelion.eu/datatxt/nex/v1/'
    chars_per_text_record = 4000

    def get_tags(self, obj):
        text = extract_text(obj)
        if not text:
            return []

        text = self._prepare_text(text)

        params = {
            'token': self.params['token'],
            'text': text,
        }

        top_entities_num = self.params.get('top_entities')
        if top_entities_num:
            params['top_entities'] = top_entities_num

        response = requests.get(self.entity_extraction_api, params)
        if response.status_code != 200:
            # TODO: Logging?
            return []

        data = response.json()

        # Remove duplicates
        entities = dict((annotation['id'], annotation) for annotation in data.get('annotations', []))
        # Sort entities by confidence
        entities = OrderedDict(sorted(entities.items(), key=lambda i: i[1]['confidence'], reverse=True))

        # If we received `topEntities` in a response,
        # this means that we can apply more accurate ordering
        # based on the Dandelion's ranking algorithm.
        top_entities = data.get('topEntities')
        if top_entities:
            entities = OrderedDict(
                ((top_entity['id'], entities[top_entity['id']]) for top_entity in top_entities)
            )

        tags = [entity['label'] for entity in entities.values()]
        return tags

    def _prepare_text(self, text):
        # Dandelion API counts usage by "Units",
        # so we should be able to limit usage
        # by defining max number of units per document.
        # See https://dandelion.eu/profile/plans-and-pricing/
        max_units = self.params.get('max_units_per_document')
        if max_units:
            length = self.chars_per_text_record * max_units
            text = Truncator(text).chars(length, truncate='')

        return text


# Shortcut
RelatedBackend = DandelionRelatedBackend
