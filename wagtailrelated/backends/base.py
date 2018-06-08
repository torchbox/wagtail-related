

class BaseRelatedBackend(object):
    def __init__(self, params):
        self.params = params

    def get_tags(self, obj):
        raise NotImplementedError("Related backend does not support the get_tags method")

    def get_similar_pages(self, obj, **kwargs):
        raise NotImplementedError("Related backend does not support the get_similar_pages method")
