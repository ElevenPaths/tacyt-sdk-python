from deprecated import deprecated

from tacyt_sdk.client import TacytClient
from tacyt_sdk.version import Version


@deprecated(version=Version.API_VERSION, action="once",
            reason="You should use TacytClient from the sdk")
class TacytApp(TacytClient):
    """Backward Compatibility with the old interface"""
    API_PROXY = None
    API_PROXY_PORT = None

    def __init__(self, app_id, secret_key, proxy=None):
        if self.API_PROXY and self.API_PROXY_PORT:
            proxy = "{}:{}".format(self.API_PROXY, self.API_PROXY_PORT)
        super(TacytApp, self).__init__(app_id, secret_key, proxy=proxy)

    @staticmethod
    def set_host(host):
        """
        :param host: The host to be connected with (http://hostname)
         or (https://hostname)
        """
        if host.startswith("https://"):
            Version.API_HOST = host[len("https://"):]

    @staticmethod
    def set_proxy(proxy, port):
        """Enable using a Proxy to connect through
        :param proxy: The proxy server
        :param port: The proxy port number
        """
        TacytApp.API_PROXY = proxy
        TacytApp.API_PROXY_PORT = port

    def search_apps(self, query, numberPage=None, maxResults=None,
                    outfields=None, grouped=None):
        return super(TacytApp, self).search_apps(
            query, number_page=numberPage, max_results=maxResults,
            outfields=outfields, grouped=grouped)

    def create_filter(self, filter):
        return super(TacytApp, self).create_filter(filter_=filter)

    def update_filter(self, filter):
        return super(TacytApp, self).update_filter(filter_=filter)

    def list_group_detected_apps(self, page, groupName):
        return super(TacytApp, self).list_group_detected_apps(
            page=page,
            group_name=groupName
        )

    def get_group_RSS_info(self, groupName):
        return super(TacytApp, self).get_group_rss_info(group_name=groupName)

    def get_RSS_info(self, filter_id):
        return super(TacytApp, self).get_rss_info(filter_id=filter_id)

    def upload_app(self, apk_file, tagName=None):
        return super(TacytApp, self).upload_app(app_path=apk_file,
                                                tag_name=tagName)

    def getEngineVersion(self, date=None, engineId=None, lang=None):
        return super(TacytApp, self).get_engine_version(
            date=date, engine_id=engineId, lang=lang)

    def uploadURL(self, urls, tagNames=None):
        return super(TacytApp, self).upload_url(urls=urls, tag_names=tagNames)
