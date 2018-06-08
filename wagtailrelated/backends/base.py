

class BaseRelatedBackend(object):
    def __init__(self, params):
        self.params = params

    def get_tags(self, obj):
        raise NotImplementedError("Related backend must implement the get_tags method")
