# More Like This API

## Request

`/api/more-like-this/?id=<page_id>&limit=<max items>&exclude=<exclusion list>`

* `id` - Required. The id of the source Wagtail Page. This will typically be the current page.
* `limit` - the maximum number of results to return. Default = `10`.
* `type` - a comma-separated list of Django content types.
  Each type must be a subclass of `wagtailcore.Page` (which is a default value).
* `exclusion list` - a comma-separated list of Wagtail Page IDs which should not included in results


### Examples

* `/api/more-like-this/?id=42&limit=5type=shops.ShopsHomePage&exclude=19,532,4`
* `/api/more-like-this/?id=42`


## Response

```json
[
  {
    "url": "https://example.com/path/page",
    "title": "2D: Drawing Studios",
    "score": 0.8,
    "type": "shops.ShopsHomePage"
  },
  {
    "url": "https://example.com/path/other-page",
    "title": "rawing",
    "score": 0.75,
    "type": "campusblog.CampusBlogPage"
  },
  {
    "url": "https://example.com/path/something-else",
    "title": "3D Printer Services",
    "score": 0.7,
    "type": "shops.ShopsHomePage"
  },
]
```


### Errors

Error response example:

```json
{
    "detail": "The ID does not match a live page"
}
```

The API will return an error in the following cases:

* No ID is provided
* The ID does not match a live page
* `limit` is more than 50 or less than 1
* `type` invalid type. Must be a subclass of `wagtailcore.Page`
* `exclude` is not a list of integers
    * integers which do not match live pages will be silently ignored


## Notes

In the initial version of the package, we will be using all text fields
to find similar pages. It’s possible to
[limit fields](https://www.elastic.co/guide/en/elasticsearch/reference/5.3/query-dsl-mlt-query.html#_document_input_parameters)
that should be used for matching, but it will be tricky
for queries where we ask for multiple content types,
because search content type has own fields. We suggest not to
include this feature in the initial version for simplicity.
We will be able to add this feature later, if we see a need
(for example, results are not relevant enough without limiting fields).

There is also no option to specify min score / threshold
in the API, but results will be returned in the order of relevance:
most relevant items will be in the beginning of a list. So the client has few options:

* Take top N elements from the list (or simply specify `limit` to be equal to N)
* Request N relevant pages and calculate “minimum relevance” using returned scores.
  Example logic: display all related pages with the
  score `doc_score >= max_score / 100 * percent`. This option is rarely useful,
  because it’s possible to get scores like `[100, 5, 3, 1]`.
  So if your `percent` is 90% you will only get one item with the score `100` .
