try:
    import urllib.parse as urllib
except ImportError:
    import urllib


class EngineVersionRequest:
    def __init__(self, date, engine_id, lang):
        self.params = [("date", date), ("engineId", engine_id), ("lang", lang)]

    def get_encoded_params(self):
        params = [(name, value) for name, value in self.params
                  if value is not None]
        return urllib.urlencode(params)
