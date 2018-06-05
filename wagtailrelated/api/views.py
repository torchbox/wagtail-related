from rest_framework import generics
from wagtail.core.models import Page

from wagtailrelated import get_autotagging_backend
from wagtailrelated.api.serializers import RelatedPageSerializer


class RelatedPagesList(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = RelatedPageSerializer

    def get_queryset(self):
        more_like_this_id = self.request.query_params.get('id')
        # TODO: Move into a proper place where we can perform validation and return errors
        # TODO: Handle PageDoesntExist
        more_like_this_page = Page.objects.live().public().filter(pk=more_like_this_id).get()

        backend = get_autotagging_backend()
        related_pages = backend._get_similar_items(more_like_this_page)

        return related_pages
