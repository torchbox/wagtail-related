import json

from wagtail.admin.widgets import AdminTagWidget


class AdminTagSuggestingWidget(AdminTagWidget):
    def render_js_init(self, id_, name, value):
        js_init = super().render_js_init(id_, name, value)

        js_init += "initTagSuggestingField({0});".format(
            json.dumps(id_),
        )

        return js_init
