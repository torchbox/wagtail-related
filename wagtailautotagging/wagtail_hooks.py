from django.conf.urls import url, include
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html
from wagtail.wagtailcore import hooks

from . import admin_urls


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^wagtailautotagging/', include(admin_urls, app_name='wagtailautotagging', namespace='wagtailautotagging')),
    ]


@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        """
            <script src="{}"></script>
        """,
        static('wagtailautotagging/js/admin_widget.js'),
    )


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        """
            <link rel="stylesheet" href="{}">
        """,
        static('wagtailautotagging/css/admin_widget.css'),
    )
