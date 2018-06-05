from __future__ import absolute_import, unicode_literals

from django.core.management.base import BaseCommand

from wagtail.core.models import Page

from wagtailrelated import get_autotagging_backend


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('page_id', type=int)
        parser.add_argument(
            '--backend',
            action='store',
            dest='backend',
            default='default',
            help='Backend name. Uses "default" backend if not specified.',
        )

    def handle(self, *args, **options):
        backend = get_autotagging_backend(options['backend'])
        page = Page.objects.get(pk=options['page_id']).specific

        tags = backend.get_tags(page)

        self.stdout.write(
            'Tags for Page(id={}):\n{}'.format(
                page.pk,
                tags,
            )
        )

        self.stdout.write('Done')
