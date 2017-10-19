from wagtail.wagtailadmin.edit_handlers import FieldPanel, BaseFieldPanel

from wagtailautotagging.widgets import AdminTagSuggestingWidget


class TagSuggestingFieldPanel(FieldPanel):
    def bind_to_model(self, model):
        base = {
            'model': model,
            'field_name': self.field_name,
            'classname': self.classname,
            'field_template': 'wagtailautotagging/edit_handlers/field_panel_field.html',
            'widget': AdminTagSuggestingWidget,
        }

        return type(str('_TagSuggestingFieldPanel'), (BaseFieldPanel,), base)
