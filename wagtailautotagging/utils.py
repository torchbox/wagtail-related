from bs4 import BeautifulSoup
from wagtail.wagtailcore.fields import StreamField


def extract_text(obj):
    """Extracts data, concatenates and removes html tags
    from fields listed in a obj.autotagging_source_fields list.
    """
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

    text = BeautifulSoup(text, 'html5lib').text
    return text
