import itertools

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from wagtail.wagtailadmin.edit_handlers import FieldPanel, BaseFieldPanel
from wagtailautotagging import get_autotagging_backend
from wagtailautotagging.widgets import AdminTagSuggestingWidget


class BaseTagSuggestingFieldPanel(BaseFieldPanel):
    field_template = 'wagtailautotagging/edit_handlers/field_panel_field.html'
    backend_name = 'default'
    suggested_tags_limit = 10

    def render_as_field(self):
        backend = get_autotagging_backend(self.backend_name)

        # TODO: Decide if we need cache here
        related_tags = None
        if self.instance and self.instance.pk:
            # Get tag suggestions
            related_tags = backend.get_tags(self.instance.get_latest_revision_as_page())

            # Get existing tags from an object
            obj_field = getattr(self.instance, self.field_name)
            existing_tags = set([tag.name for tag in obj_field.all()])

            # Create a generator that excludes tags that already exist in the current field
            related_tags = (element for element in related_tags if element not in existing_tags)

            # Do not render all tags: use only most relevant ones
            related_tags = list(itertools.islice(related_tags, self.suggested_tags_limit))

        context = {
            'field': self.bound_field,
            'field_type': self.field_type(),
            'related_tags': related_tags,
        }
        return mark_safe(render_to_string(self.field_template, context))


class TagSuggestingFieldPanel(FieldPanel):
    def __init__(self, *args, **kwargs):
        self.suggested_tags_limit = kwargs.pop('suggested_tags_limit', None)
        self.backend_name = kwargs.pop('backend_name', None)

        super().__init__(*args, **kwargs)

    def bind_to_model(self, model):
        base = {
            'model': model,
            'field_name': self.field_name,
            'classname': self.classname,
            'widget': AdminTagSuggestingWidget,
        }
        if self.suggested_tags_limit:
            base['suggested_tags_limit'] = self.suggested_tags_limit

        if self.backend_name:
            base['backend_name'] = self.backend_name

        return type(str('_TagSuggestingFieldPanel'), (BaseTagSuggestingFieldPanel,), base)
