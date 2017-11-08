import itertools
from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from wagtail.wagtailcore.models import Page

from wagtailautotagging import get_autotagging_backend


class SuggestTagsOnEditView(View):
    http_method_names = ('post', )

    def post(self, request, pk):
        content_type = request.GET['content_type']
        field_name = request.GET['field_name']
        backend_name = request.GET['backend_name']
        tags_limit = int(request.GET['tags_limit'])

        model = self.get_model(content_type)
        obj = self.get_object(model, pk)
        form = self.get_form(obj)

        if not form.is_valid():
            # TODO: return an error
            return JsonResponse({})

        # We need to suggest tags based on the current state of the form
        # we don't need to save the instance
        obj = form.save(commit=False)

        backend = get_autotagging_backend(backend_name)

        # Get tag suggestions
        related_tags = backend.get_tags(obj)

        # Get existing tags from an object
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

    def get_form(self, page):
        # TODO: Check if it's possible make it more generic (to serve non-Page objects)

        form_class = page.get_edit_handler().get_form_class(page._meta.model)
        parent_page = page.get_parent().specific

        return form_class(self.request.POST, instance=page, parent_page=parent_page)

    @staticmethod
    def get_model(content_type):
        app_label, model = content_type.split('.', 1)

        return apps.get_model(app_label, model)

    def get_object(self, model, pk):
        obj = get_object_or_404(model, pk=pk)

        # Return the latest revision, if it's a page
        if issubclass(model, Page):
            obj = obj.get_latest_revision_as_page()

        return obj


class SuggestTagsOnCreateView(SuggestTagsOnEditView):
    # TODO: Fix signature
    def post(self, request, parent_pk):
        return super().post(request, parent_pk)

    def get_object(self, model, pk):
        # pk is parent_page_pk when we create a new page
        parent_page_id = pk

        page = model()
        parent_page = get_object_or_404(Page, id=parent_page_id).specific
        # We need to populate treebeard's path / depth fields in order to
        # pass validation. We can't make these 100% consistent with the rest
        # of the tree without making actual database changes (such as
        # incrementing the parent's numchild field), but by calling treebeard's
        # internal _get_path method, we can set a 'realistic' value that will
        # hopefully enable tree traversal operations
        # to at least partially work.
        page.depth = parent_page.depth + 1
        # Puts the page at the maximum possible path
        # for a child of `parent_page`.
        page.path = Page._get_children_path_interval(parent_page.path)[1]
        return page

    def get_form(self, page):
        form = super().get_form(page)
        if form.is_valid():
            # Ensures our unsaved page has a suitable url.
            form.instance.set_url_path(form.parent_page)

            form.instance.full_clean()
        return form
