import itertools

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from wagtail.admin.edit_handlers import FieldPanel

from wagtailrelated import get_backend
from wagtailrelated.widgets import AdminTagSuggestingWidget


class TagSuggestingFieldPanel(FieldPanel):

    def __init__(
        self, field_name, heading='', classname='', help_text='',
        suggested_tags_limit=10, backend_name='default',
        *args, **kwargs
    ):
        # Default widget
        self.widget = AdminTagSuggestingWidget

        super().__init__(field_name, *args, **kwargs)
        self.heading = heading
        self.classname = classname
        self.help_text = help_text
        self.suggested_tags_limit = suggested_tags_limit
        self.backend_name = backend_name

    def clone(self):
        return self.__class__(
            field_name=self.field_name,
            widget=self.widget,
            heading=self.heading,
            classname=self.classname,
            help_text=self.help_text,
            suggested_tags_limit=self.suggested_tags_limit,
            backend_name=self.backend_name,
        )

    object_template = "wagtailrelated/edit_handlers/single_field_panel.html"

    def render_as_object(self):
        return mark_safe(render_to_string(self.object_template, {
            'self': self,
            self.TEMPLATE_VAR: self,
            'field': self.bound_field,
            'related_tags': self.get_related_tags(),
        }))

    field_template = 'wagtailrelated/edit_handlers/field_panel_field.html'

    def render_as_field(self):
        context = {
            'field': self.bound_field,
            'field_type': self.field_type(),
            'related_tags': self.get_related_tags(),
        }
        return mark_safe(render_to_string(self.field_template, context))

    def get_related_tags(self):
        backend = get_backend(self.backend_name)

        # TODO: Decide if we need cache here
        related_tags = None
        if self.instance and self.instance.pk:
            # Get tag suggestions
            related_tags = backend.get_tags(self.instance)

            # Get existing tags from an object
            obj_field = getattr(self.instance, self.field_name)
            existing_tags = set([tag.name for tag in obj_field.all()])

            # Create a generator that excludes tags that already exist in the current field
            related_tags = (element for element in related_tags if element not in existing_tags)

            # Do not render all tags: use only most relevant ones
            related_tags = list(itertools.islice(related_tags, self.suggested_tags_limit))

        return related_tags
