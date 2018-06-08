from rest_framework import generics
from rest_framework.response import Response
from wagtail.api.v2.utils import page_models_from_string
from wagtail.core.models import Page

from wagtailrelated import get_backend
from wagtailrelated.api.exceptions import BadRequestError
from wagtailrelated.api.serializers import RelatedPageSerializer


class RelatedPagesList(generics.ListAPIView):
    queryset = Page.objects.live().public()
    serializer_class = RelatedPageSerializer

    min_limit = 1
    max_limit = 50

    def list(self, request):
        more_like_this_id = self.request.query_params.get('id')
        limit = self.request.query_params.get('limit', 20)
        content_type = self.request.query_params.get('type', 'wagtailcore.Page')
        exclude_ids = self.request.query_params.get('exclude')

        if more_like_this_id is None:
            raise BadRequestError('No ID is provided')

        queryset = self.get_queryset()
        try:
            more_like_this_page = queryset.filter(pk=more_like_this_id).get()
        except queryset.model.DoesNotExist:
            raise BadRequestError('The ID does not match a live page')

        try:
            models = page_models_from_string(content_type)
        except (LookupError, ValueError):
            raise BadRequestError("type doesn't exist")

        try:
            limit = int(limit)
        except ValueError:
            raise BadRequestError('Limit is not an integer')

        if not self.min_limit <= limit <= self.max_limit:
            raise BadRequestError('Limit is less than {} or more than {}'.format(self.min_limit, self.max_limit))

        exclude_ids = exclude_ids.split(',') if exclude_ids else []
        if len(exclude_ids) > 0:
            for i, val in enumerate(exclude_ids):
                try:
                    exclude_ids[i] = int(val)
                except ValueError:
                    raise BadRequestError('exclude is not a list of integers')

        backend = get_backend()
        related_pages = backend.get_similar_items(
            more_like_this_page,
            limit=limit,
            content_types=models,
            exclude_pks=exclude_ids,
        )

        serializer = self.serializer_class(related_pages, many=True)
        return Response(serializer.data)
