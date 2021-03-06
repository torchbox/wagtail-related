from bs4 import BeautifulSoup
from wagtail.core.fields import StreamField


def extract_text(obj):
    """Extracts data, concatenates and removes html tags
    from fields listed in a obj.related_source_fields list.
    """
    related_source_fields = getattr(obj._meta.model, 'related_source_fields', None)
    if not related_source_fields:
        return

    html_pieces = []
    for source_field in related_source_fields:
        field = source_field.get_field(obj.__class__)
        field_value = source_field.get_value(obj)
        if isinstance(field, StreamField):
            field_value = ' '.join(field_value)

        html_pieces.append(field_value)

    text = ' '.join(html_pieces)

    text = BeautifulSoup(text, 'html5lib').text
    return text
