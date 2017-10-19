from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.wagtailadmin.edit_handlers import FieldPanel, BaseFieldPanel

from wagtailautotagging import get_autotagging_backend
from wagtailautotagging.widgets import AdminTagSuggestingWidget


class BaseTagSuggestingFieldPanel(BaseFieldPanel):
    field_template = 'wagtailautotagging/edit_handlers/field_panel_field.html'
    backend_name = 'default'

    def render_as_field(self):
        backend = get_autotagging_backend(self.backend_name)

        # TODO: Decide if we need cache here
        related_tags = None
        if self.instance and self.instance.pk:
            # Get tag suggestions
            related_tags = set(backend.get_tags(self.instance))

            # Get existing tags from a page
            obj_field = getattr(self.instance, self.field_name)
            existing_tags = set([tag.name for tag in obj_field.all()])

            # Exclude tags that already exist
            related_tags = related_tags - existing_tags

        context = {
            'field': self.bound_field,
            'field_type': self.field_type(),
            'related_tags': related_tags,
        }
        return mark_safe(render_to_string(self.field_template, context))


class TagSuggestingFieldPanel(FieldPanel):
    def bind_to_model(self, model):
        base = {
            'model': model,
            'field_name': self.field_name,
            'classname': self.classname,
            'widget': AdminTagSuggestingWidget,
        }

        return type(str('_TagSuggestingFieldPanel'), (BaseTagSuggestingFieldPanel,), base)
