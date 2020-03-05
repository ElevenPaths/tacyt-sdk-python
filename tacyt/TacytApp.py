from deprecated import deprecated

from tacyt_sdk.client import TacytClient
from tacyt_sdk.version import Version


@deprecated(version="2.7", action="once", reason="You should use TacytClient from the sdk")
class TacytApp(TacytClient):
    """Backward Compatibility with the old interface"""
    API_PROXY = None
    API_PROXY_PORT = None
    API_HOST = None
    API_VERSION = None

    def __init__(self, app_id, secret_key, api_host=None, api_version=None,
                 proxy=None):
        if self.API_PROXY and self.API_PROXY_PORT:
            proxy = "{}:{}".format(self.API_PROXY, self.API_PROXY_PORT)
        api_host = api_host or Version.API_HOST
        api_version = api_version or Version.API_VERSION
        super(TacytApp, self).__init__(app_id, secret_key,
                                       api_host,
                                       api_version,
                                       proxy)

    def compose_url(self, url):
        """Compose the final url with the schema and the host of
        the api endpoint.
        :param url: the url path to the endpoint to reach
        :type url: str
        :return: A full composed http(s) url to call.
        """
        return "https://" + Version.API_HOST + url

    @property
    def base_url(self):
        return "/api/" + Version.API_VERSION + "/{endpoint}"

    @staticmethod
    def set_host(host):
        """Set the host to use.
        NOTE: use the new api_host to set if the object is already created.
        :param host: The host to be connected with (https://hostname)
        """
        if host.startswith("https://"):
            Version.API_HOST = host[len("https://"):]

    @staticmethod
    def set_version(version):
        """Set the version of the api to use.
        NOTE: use the new api_version to set if the object is already created.
        :param version: The api version to be used.
        """
        Version.API_VERSION = version

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
        """
        :param query: The query string will filter the search results
        :param numberPage: $numberPage A number greater or equal to 1
        indicating the page of results which have to be retrieved
        :param maxResults: A number between 1 and 100 indicating the max
        number of apps which have to be retrieved
        :param outfields: the set of fields that will return form the api
        :param grouped: if you want to grouped the same applications
        :return: Json structure with the keys to the Applications found
        """
        return super(TacytApp, self).search_apps(
            query, number_page=numberPage, max_results=maxResults,
            outfields=outfields, grouped=grouped)

    def create_filter(self, filter):
        """This method create a filter.
        :param filter: A filter object to create
        :return: Response object with the filter structure
        """
        return super(TacytApp, self).create_filter(filter)

    def update_filter(self, filter):
        """This method update changes associates with a filter.
        :param filter: Filter structure to update
        """
        return super(TacytApp, self).update_filter(filter)

    def list_group_detected_apps(self, page, groupName):
        """Get the detected apps by a group.
        :param page: A number greater or equal to 1 indicating the page of
        results which have to be retrieved
        :param groupName: name of the group
        :return: Response object with the details of applications detected by
        the filters group
        """
        return super(TacytApp, self).list_group_detected_apps(
            page=page,
            group_name=groupName
        )

    def get_group_RSS_info(self, groupName):
        """This method get the RSS information of a filters group
        :param groupName: name of the filters group you want get RSS
        information.
        :return: Response object with the rss information of the filters
        of a group.
        """
        return super(TacytApp, self).get_group_rss_info(group_name=groupName)

    def get_RSS_info(self, filter_id):
        """This method get the RSS information of a filter.
        :param filter_id: id to filter you want get RSS information
        :return: Response object with the information of a filter.
        """
        return super(TacytApp, self).get_rss_info(filter_id=filter_id)

    def upload_app(self, apk_file, tagName=None):
        """Upload an app file to Tacyt
        :param apk_file: path to file apk
        :param tagName: an optional tag to labeled the uploaded app.
        :return: Response object.
        """
        return super(TacytApp, self).upload_app(app_path=apk_file,
                                                tag_name=tagName)

    def getEngineVersion(self, date=None, engineId=None, lang=None):
        """Search an engine and its associated vulnerabilities.
        If no params return a list of all existing engines
        :param engineId: engine id.
        :param date: search the engine available on that date.
        :param lang: output language of vulnerabilities fields.
        Values "es" or "en"
        :return: Response
        """
        return super(TacytApp, self).get_engine_version(
            date=date, engine_id=engineId, lang=lang)

    def uploadURL(self, urls, tagNames=None):
        """Download apps from a market URLs
        :param urls: List of urls to upload
        :param tagNames List of tags to identify the application
        :return: Response object
        """
        return super(TacytApp, self).upload_url(urls=urls, tag_names=tagNames)
