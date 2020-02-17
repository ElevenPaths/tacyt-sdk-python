from deprecated import deprecated

from tacyt_sdk.client import TacytClient
from tacyt_sdk.version import Version


class TacytApp(TacytClient):
    """Backward Compatibility with the old interface"""
    @deprecated(version=Version.API_VERSION,
                reason="You should use TacytClient from the sdk")
    def __init__(self, app_id, secret_key):
        super(TacytApp, self).__init__(app_id, secret_key)

    @deprecated(version=Version.API_VERSION,
                reason="You should use TacytClient from the sdk")
    def search_apps(self, query, numberPage=None, maxResults=None,
                    outfields=None, grouped=None):
        super(TacytApp, self).search_apps(
            query, number_page=numberPage, max_results=maxResults,
            outfields=outfields, grouped=grouped)

    @deprecated(version=Version.API_VERSION,
                reason="You should use TacytClient from the sdk")
    def create_filter(self, filter):
        return super(TacytApp, self).create_filter(filter_=filter)

    @deprecated(version=Version.API_VERSION,
                reason="You should use TacytClient from the sdk")
    def update_filter(self, filter):
        return super(TacytApp, self).update_filter(filter_=filter)

    @deprecated(version=Version.API_VERSION,
                reason="You should use TacytClient from the sdk")
    def list_group_detected_apps(self, page, groupName):
        return super(TacytApp, self).list_group_detected_apps(
            page=page,
            group_name=groupName
        )

    @deprecated(version=Version.API_VERSION,
                reason="You should use TacytClient from the sdk")
    def get_group_RSS_info(self, groupName):
        return super(TacytApp, self).get_group_RSS_info(group_name=groupName)

    @deprecated(version=Version.API_VERSION,
                reason="You should use TacytClient from the sdk")
    def upload_app(self, apk_file, tagName=None):
        return super(TacytApp, self).upload_app(app_path=apk_file,
                                                tag_name=tagName)

    @deprecated(version=Version.API_VERSION,
                reason="You should use TacytClient from the sdk")
    def getEngineVersion(self, date=None, engineId=None, lang=None):
        return super(TacytApp, self).get_engine_version(
            date=date, engine_id=engineId, lang=lang)

    @deprecated(version=Version.API_VERSION,
                reason="You should use TacytClient from the sdk")
    def uploadURL(self, urls, tagNames=None):
        return super(TacytApp, self).uploadURL(urls=urls, tag_names=tagNames)
