from django.utils.text import Truncator
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2.service_account import Credentials

from wagtailautotagging.backends.base import BaseAutotaggingBackend
from wagtailautotagging.utils import extract_text


class GoogleCloudLanguageAutotaggingBackend(BaseAutotaggingBackend):
    chars_per_text_record = 1000

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        credentials = Credentials.from_service_account_file(self.params['service_account_json'])
        credentials = credentials.with_scopes(('https://www.googleapis.com/auth/cloud-platform',))
        self.client = language.LanguageServiceClient(credentials=credentials)

    def get_tags(self, obj):
        text = extract_text(obj)
        if not text:
            return []

        text = self._prepare_text(text)

        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT
        )

        entities = self.client.analyze_entities(document=document).entities
        tags = [entity.name for entity in entities]

        return tags

    def _prepare_text(self, text):
        # Google Natural Language API counts usage by "Text records",
        # so we should be able to limit usage
        # by defining max number of text records per document.
        # See https://cloud.google.com/natural-language/pricing
        max_text_records = self.params.get('max_text_records_per_document')
        if max_text_records:
            length = self.chars_per_text_record * max_text_records
            text = Truncator(text).chars(length, truncate='')

        return text


# Shortcut
AutotaggingBackend = GoogleCloudLanguageAutotaggingBackend
