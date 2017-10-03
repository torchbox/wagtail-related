

class BaseAutotaggingBackend(object):
    def __init__(self, params):
        self.params = params

    def get_tags(self, page):
        raise NotImplementedError("Autotagging backend must implement the get_tags method")
