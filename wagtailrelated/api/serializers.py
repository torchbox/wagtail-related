from rest_framework import serializers
from rest_framework.fields import Field
from wagtail.api.v2.serializers import PageHtmlUrlField
from wagtail.core.models import Page


class PageTypeField(Field):
    """
    Serializes the "type" field for pages.

    This takes into account the fact that we sometimes may not have the "specific"
    page object by calling "page.specific_class" instead of looking at the object's
    type.

    Example:
    "type": "blog.BlogPage"
    """
    def get_attribute(self, instance):
        return instance

    def to_representation(self, page):
        name = page.specific_class._meta.app_label + '.' + page.specific_class.__name__
        return name


class RelatedPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'title', 'type', 'url')

    # TODO: Add the score field
    type = PageTypeField()
    url = PageHtmlUrlField()
