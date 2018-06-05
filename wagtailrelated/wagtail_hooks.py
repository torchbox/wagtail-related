from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html
from wagtail.core import hooks


@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        """
            <script src="{}"></script>
        """,
        static('wagtailrelated/js/admin_widget.js'),
    )


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        """
            <link rel="stylesheet" href="{}">
        """,
        static('wagtailrelated/css/admin_widget.css'),
    )
