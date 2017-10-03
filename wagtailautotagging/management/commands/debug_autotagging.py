from __future__ import absolute_import, unicode_literals

from django.core.management.base import BaseCommand

from wagtail.wagtailcore.models import Page

from wagtailautotagging import get_autotagging_backend


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('page_id', type=int)

    def handle(self, *args, **options):
        backend = get_autotagging_backend()
        page = Page.objects.get(pk=options['page_id']).specific

        tags = backend.get_tags(page)

        self.stdout.write(
            'Tags for Page(id={}):\n{}'.format(
                page.pk,
                tags,
            )
        )

        self.stdout.write('Done')
