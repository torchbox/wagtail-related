from bs4 import BeautifulSoup
from django.utils.text import Truncator
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2.service_account import Credentials
from wagtail.wagtailcore.fields import StreamField

from wagtailautotagging.backends.base import BaseAutotaggingBackend


class GoogleCloudLanguageAutotaggingBackend(BaseAutotaggingBackend):
    CHARS_PER_TEXT_RECORD = 1000

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        credentials = Credentials.from_service_account_file(self.params['service_account_json'])
        credentials = credentials.with_scopes(('https://www.googleapis.com/auth/cloud-platform',))
        self.client = language.LanguageServiceClient(credentials=credentials)

    def get_tags(self, obj):
        text = self._extract_text(obj)
        text = self._prepare_text(text)
        if not text:
            return

        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT
        )

        entities = self.client.analyze_entities(document=document).entities
        tags = [entity.name for entity in entities]

        return tags

    def _extract_text(self, obj):
        autotagging_source_fields = getattr(obj._meta.model, 'autotagging_source_fields', None)
        if not autotagging_source_fields:
            return

        html_pieces = []
        for source_field in autotagging_source_fields:
            field = source_field.get_field(obj.__class__)
            field_value = source_field.get_value(obj)
            if isinstance(field, StreamField):
                field_value = ' '.join(field_value)

            html_pieces.append(field_value)

        text = ' '.join(html_pieces)
        return text

    def _prepare_text(self, text):
        if not text:
            return text

        # Remove all html tags and leave text only
        # to reduce Google Natural Language API usage
        text = BeautifulSoup(text, 'html5lib').text

        # Google Natural Language API counts usage by "Text records",
        # so we should be able to limit usage
        # by defining max number text records per document
        max_text_records = self.params.get('max_text_records_per_document')
        if max_text_records:
            length = self.CHARS_PER_TEXT_RECORD * max_text_records
            text = Truncator(text).chars(length, truncate='')

        return text


# Shortcut
AutotaggingBackend = GoogleCloudLanguageAutotaggingBackend
