# wagtailrelated

A module for Wagtail that finds related pages and tags for your pages.

## How to install

Install using pip:

```
pip install wagtail-related
```


### Settings

In your settings file, add `wagtailrelated` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'wagtailrelated',
    # ...
]
```

### URL configuration

Include API url into your `urlpatterns`:

```python
urlpatterns = [
    # ...
    url(r'^api/more-like-this', include('wagtailrelated.api.urls')),
    # ...
```

### Backend settings

Add the following setting into your project:

```python
WAGTAIL_RELATED_BACKENDS = {
    'default': {
        'BACKEND': 'wagtailrelated.backends.elasticsearch5',
    }
}
```

Note that the module uses Elasticsearch to find related pages and relies on Wagtail's
built-in search backend. This means that you should have the
[`WAGTAILSEARCH_BACKENDS` setting](http://docs.wagtail.io/en/v2.1/topics/search/backends.html#elasticsearch-backend)
comfigured with `wagtail.search.backends.elasticsearch5` in your project.

Settings shown in this instruction will work fine,
if your Elasticsearch 5 backend exists under the `default` key.
If your project has multiple Wagtail search backends and your Elasticsearch 5 search backend
has different key, see how you need to modify `WAGTAIL_RELATED_BACKENDS`
[here](https://github.com/torchbox/wagtail-related/blob/master/docs/related_backends.md#set-up-wagtail_related_backends-use-non-default-search-backend).

## How to use

The package provides an API to get related pages. See the
[API documentation](https://github.com/torchbox/wagtail-related/blob/master/docs/api.md).
