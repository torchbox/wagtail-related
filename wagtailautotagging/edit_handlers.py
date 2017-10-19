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

        related_tags = None
        if self.instance and self.instance.pk:
            # TODO: Decide if we need cache here
            # TODO: Exclude tags that already exist
            related_tags = backend.get_tags(self.instance)

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
