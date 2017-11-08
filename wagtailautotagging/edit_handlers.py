import urllib.parse

from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe

from wagtail.wagtailadmin.edit_handlers import FieldPanel, BaseFieldPanel
from wagtailautotagging.widgets import AdminTagSuggestingWidget


class BaseTagSuggestingFieldPanel(BaseFieldPanel):
    field_template = 'wagtailautotagging/edit_handlers/field_panel_field.html'
    backend_name = 'default'
    suggested_tags_limit = 10

    def render_as_field(self):
        query_data = {
            'content_type': self.instance._meta.label,
            'field_name': self.field_name,
            'backend_name': self.backend_name,
            'tags_limit': self.suggested_tags_limit,
        }

        if self.instance and self.instance.pk:
            # It's an existing object
            suggest_tags_url = reverse(
                'wagtailautotagging:suggest_tags_on_edit',
                kwargs={'pk': self.instance.pk}
            )
        else:
            # It's a new object
            # TODO: Review it
            # To suggest tags on page creation we have to pass parent page id.
            # We do that using `self.bound_field.form.parent_page`
            # which is hacky way, but I can't think of better way, at the moment.
            suggest_tags_url = reverse(
                'wagtailautotagging:suggest_tags_on_create',
                kwargs={'parent_pk': self.bound_field.form.parent_page.pk}
            )

        suggest_tags_url += '?' + urllib.parse.urlencode(query_data)

        context = {
            'field': self.bound_field,
            'field_type': self.field_type(),
            'suggest_tags_url': suggest_tags_url,
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
