# Related backends

This document describes possible configuration options and back-end specific features.

## Elasticsearch 5 backend


### Set up `WAGTAIL_RELATED_BACKENDS` use non-`default` search backend

Some projects have multiple search backends and it's possible
that the Elasticsearch 5 search backend you want to use has a key other than `default`
in `WAGTAIL_RELATED_BACKENDS`. It's possible to change `WAGTAIL_RELATED_BACKENDS` to reflect it.

Here is an example of `WAGTAILSEARCH_BACKENDS`:

```python
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.contrib.postgres_search.backend',
    },
    'elasticsearch_key': {
        'BACKEND': 'wagtail.search.backends.elasticsearch5',
        # Other ES search back-end parameters like URLS, INDEX, etc
    },
}
```

In this case, you need to add the `wagtailsearch_backend` parameter to your
related backend definition like this:

```python
WAGTAIL_RELATED_BACKENDS = {
    'default': {
        'BACKEND': 'wagtailrelated.backends.elasticsearch5',
        'wagtailsearch_backend': 'elasticsearch_key',
    }
}
```

### How Elasticsearch related backend works

Under the hood the backend uses the
[`more_like_this` query](https://www.elastic.co/guide/en/elasticsearch/reference/5.6/query-dsl-mlt-query.html).
Currently it uses all text fields to find similar docuemnts. It is possible that we will change this behaviour.
