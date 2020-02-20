from datetime import datetime

try:
    import urllib.parse as urllib
except ImportError:
    import urllib

from tacyt_sdk.utils import datetime_isoformat


class EngineVersionRequest(object):
    def __init__(self, date, engine_id, lang):
        converted_date = date
        if isinstance(date, datetime):
            converted_date = datetime_isoformat(date)

        self.params = [("date", converted_date), ("engineId", engine_id),
                       ("lang", lang)]

    def get_encoded_params(self):
        params = sorted([(name, value) for name, value in self.params
                         if value is not None])
        return urllib.urlencode(params)
