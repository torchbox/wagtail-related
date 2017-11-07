import itertools
from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from wagtail.wagtailcore.models import Page

from wagtailautotagging import get_autotagging_backend


class SuggestTagsView(View):
    def get(self, request, pk):
        content_type = request.GET['content_type']
        field_name = request.GET['field_name']
        backend_name = request.GET['backend_name']
        tags_limit = int(request.GET['tags_limit'])

        model = self.get_model(content_type)
        obj = self.get_object(model, pk)
        backend = get_autotagging_backend(backend_name)

        # Get tag suggestions
        related_tags = backend.get_tags(obj)

        # Get existing tags from a page
        obj_field = getattr(obj, field_name)
        existing_tags = set([tag.name for tag in obj_field.all()])

        # Create a generator that excludes tags that already exist in the current field
        related_tags = (element for element in related_tags if element not in existing_tags)

        # Do not render all tags: use only most relevant ones
        related_tags = list(itertools.islice(related_tags, tags_limit))

        data = {
            'suggested_tags': related_tags
        }

        return JsonResponse(data)

    @staticmethod
    def get_model(content_type):
        app_label, model = content_type.split('.', 1)

        return apps.get_model(app_label, model)

    @staticmethod
    def get_object(model, pk):
        obj = get_object_or_404(model, pk=pk)

        # Return the latest revision, if it's a page
        if issubclass(model, Page):
            obj = obj.get_latest_revision_as_page()

        return obj
