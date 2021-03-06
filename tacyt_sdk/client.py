import hashlib
import logging
from os import path

from tacyt_sdk.api_requests.compare_request import CompareRequest
from tacyt_sdk.api_requests.engine_version_request import EngineVersionRequest
from tacyt_sdk.api_requests.filter_request import FilterRequest
from tacyt_sdk.api_requests.market_app_request import (NewMarketAppRequest,
                                                       UpdateMarketAppRequest)
from tacyt_sdk.api_requests.search_request import SearchRequest
from tacyt_sdk.api_requests.tag_request import TagRequest
from tacyt_sdk.api_requests.upload_url_request import UploadUrlRequest
from tacyt_sdk.authorization.auth import Auth
from tacyt_sdk.filter_model import Filter


logger = logging.getLogger(__name__)


class TacytClient(Auth):
    def __init__(self, app_id, secret_key, api_host=None, api_version=None,
                 proxy=None):
        """Create an instance of the class with the Application ID and secret
         obtained from Tacyt.
        :param app_id: the app id part of your credentials
        :param secret_key: the secret part of your credentials
        """
        super(TacytClient, self).__init__(app_id, secret_key,
                                          api_host,
                                          api_version,
                                          proxy)

    @property
    def base_url(self):
        return "/api/" + self.api_version + "/{endpoint}"

    @property
    def API_SEARCH_URL(self):
        return self.base_url.format(endpoint="search")

    @property
    def API_DETAILS_URL(self):
        return self.base_url.format(endpoint="details")

    @property
    def API_FILTERS_URL(self):
        return self.base_url.format(endpoint="filters")

    @property
    def API_TAGS_URL(self):
        return self.base_url.format(endpoint="tags")

    @property
    def API_COMPARER_URL(self):
        return self.base_url.format(endpoint="compare")

    @property
    def API_UPLOAD_URL(self):
        return self.base_url.format(endpoint="upload")

    @property
    def API_ENGINE_VERSION_URL(self):
        return self.base_url.format(endpoint="engineVersion")

    @property
    def API_UPLOADURL_URL(self):
        return self.base_url.format(endpoint="uploadURL")

    @property
    def API_MARKET_URL(self):
        return self.base_url.format(endpoint="app")

    def search_apps(self, query, number_page=None, max_results=None,
                    outfields=None, grouped=None):
        """
        :param query: The query string will filter the search results
        :param number_page: $numberPage A number greater or equal to 1
        indicating the page of results which have to be retrieved
        :param max_results: A number between 1 and 100 indicating the max
        number of apps which have to be retrieved
        :param outfields: the set of fields that will return form the api
        :param grouped: if you want to grouped the same applications
        :return: Json structure with the keys to the Applications found
        """
        result = SearchRequest(query, number_page, max_results,
                               outfields, grouped)
        return self.http_post(self.API_SEARCH_URL, body=result.as_dict())

    def get_app_details(self, key):
        """
        :param key: The key of an application
        :return: Json structure with the details of an application
        """
        url = self.API_DETAILS_URL + "/" + key
        return self.http_get(url)

    def list_tags(self):
        """
        :return: A list of tags that have been created.
        """
        result = TagRequest(TagRequest.LIST_REQUEST, None, None)
        return self.http_post(self.API_TAGS_URL, body=result.as_dict())

    def assign_tag(self, tag, app_keys):
        """This method associates a tag created with applications.
        :param tag: the name of the tag to create
        :param app_keys: Key applications that want to associate with the tag
        :return: applications associates with a tag
        :rtype: list
        """
        """
        This method associates a tag created with applications.
        @param $tag the name of the tag to create
        @param $app_keys Key applications that want to associate with the tag
        @return A list of applications associates with a tag.
        """
        result = TagRequest(TagRequest.CREATE_REQUEST, tag, app_keys)
        return self.http_post(self.API_TAGS_URL, body=result.as_dict())

    def remove_tag_for_apps(self, tag, app_keys):
        """This method remove a tag associate with applications.
        :param tag: the name of the tag to create
        :param app_keys: Key applications that want to remove with the tag
        :return:
        """
        result = TagRequest(TagRequest.REMOVE_REQUEST, tag, app_keys)
        return self.http_post(self.API_TAGS_URL, body=result.as_dict())

    def delete_tag(self, tag):
        """This method delete a tag.
        :param tag: the name of the tag you want to delete
        :return: A response object.
        """
        result = TagRequest(TagRequest.REMOVE_ALL_REQUEST, tag, None)
        return self.http_post(self.API_TAGS_URL, body=result.as_dict())

    def create_filter(self, filter_object):
        """This method create a filter.
        :param filter_object: A filter object to create
        :return: Response object with the filter structure
        """
        result = FilterRequest(FilterRequest.CREATE_REQUEST, filter_object,
                               0, None)
        return self.http_post(self.API_FILTERS_URL, body=result.as_dict())

    def update_filter(self, filter_object):
        """This method update changes associates with a filter.
        :param filter_object: Filter structure to update
        """
        result = FilterRequest(FilterRequest.UPDATE_REQUEST, filter_object,
                               0, None)
        return self.http_post(self.API_FILTERS_URL, body=result.as_dict())

    def read_group_filters(self):
        """Get all the filters that belongs to a group.
        :return: all group filters created
        """
        result = FilterRequest(FilterRequest.READ_GROUPS, None, 0, None)
        return self.http_post(self.API_FILTERS_URL, body=result.as_dict())

    def read_all_filters(self):
        """Get all the existing filters.
        :return: a list of filters creates.
        """
        result = FilterRequest(FilterRequest.READ_REQUEST, None, 0, None)
        return self.http_post(self.API_FILTERS_URL, body=result.as_dict())

    def read_one_filter(self, filter_id):
        """Get a filter with a filter_id
        :param filter_id: id of the filter you want to read
        :return: This method returns the details of filter associate with this
        filter_id.
        """
        filter_ = Filter(filter_id)
        result = FilterRequest(FilterRequest.READ_REQUEST, filter_, 0, None)
        return self.http_post(self.API_FILTERS_URL, body=result.as_dict())

    def delete_filter(self, filter_id):
        """This method delete a filter create.
        :param filter_id: id of the filter you want to delete
        """
        filter_ = Filter(filter_id)
        result = FilterRequest(FilterRequest.DELETE_REQUEST, filter_, 0, None)
        return self.http_post(self.API_FILTERS_URL, body=result.as_dict())

    def search_public_filter(self, query, page):
        """Search and retrieves public filters that match with the query.
        :param query: any word or phrase within the description or title Filter
        :param page: A number greater or equal to 1 indicating the page of
        results which have to be retrieved.
        :return: A list of public filters(Visibility = Public)
        """
        result = FilterRequest(FilterRequest.SEARCH_PUBLIC_FILTER_REQUEST,
                               None, page, query)
        return self.http_post(self.API_FILTERS_URL, body=result.as_dict())

    def list_detected_apps(self, page, filter_id):
        """Get the detected apps by a filter.
        :param page:
        :param filter_id: id to the filter.
        :return: Response object with the details of applications detected by
        the filter.
        """
        result = FilterRequest(FilterRequest.LIST_DETECTIONS_REQUEST,
                               None, page, filter_id)
        return self.http_post(self.API_FILTERS_URL, body=result.as_dict())

    def list_group_detected_apps(self, page, group_name):
        """Get the detected apps by a group.
        :param page: A number greater or equal to 1 indicating the page of
        results which have to be retrieved
        :param group_name: name of the group
        :return: Response object with the details of applications detected by
        the filters group
        """
        result = FilterRequest(FilterRequest.LIST_GROUP_DETECTIONS, None, page,
                               group_name)
        return self.http_post(self.API_FILTERS_URL, body=result.as_dict())

    def unsubscribe_public_filter(self, filter_id):
        """Unsubscribe to a filter.
        :param filter_id: id of the filter you want subscribe.
        """
        result = FilterRequest(FilterRequest.UNSUBSCRIBE_REQUEST, None, 0,
                               filter_id)
        return self.http_post(self.API_FILTERS_URL, body=result.as_dict())

    def subscribe_public_filter(self, filter_id):
        """Subscribe to filter
        With this method you can unsubscribe to filter.
        :param filter_id: id of the filter you want to unsubscribe
        """
        result = FilterRequest(FilterRequest.SUBSCRIBE_REQUEST, None, 0,
                               filter_id)
        return self.http_post(self.API_FILTERS_URL, body=result.as_dict())

    def get_rss_info(self, filter_id):
        """This method get the RSS information of a filter.
        :param filter_id: id to filter you want get RSS information
        :return: Response object with the information of a filter.
        """
        result = FilterRequest(FilterRequest.GET_RSS_REQUEST, None, None,
                               filter_id)
        return self.http_post(self.API_FILTERS_URL, body=result.as_dict())

    def get_group_rss_info(self, group_name):
        """This method get the RSS information of a filters group
        :param group_name: name of the filters group you want get RSS
        information.
        :return: Response object with the rss information of the filters
        of a group.
        """
        result = FilterRequest(FilterRequest.GET_GROUP_RSS, None, None,
                               content=group_name)
        return self.http_post(self.API_FILTERS_URL, body=result.as_dict())

    def compare_apps(self, apps, include_details):
        """Compare between two or more apps.
        :param apps: the key of the app you want to compare.
        The array of apps is limited to 10 apps.
        :param include_details: with a value of true in $include_details
        you will get not only the matching fields and their values
        but all the values defined for the applications.
        :return: Response object with the comparison between the apps.
        """
        result = CompareRequest(apps, include_details)
        return self.http_post(self.API_COMPARER_URL, body=result.as_dict())

    def upload_app(self, app_path, tag_name=None, send_to_av_date=None):
        """Upload an app file to Tacyt
        :param app_path: path to file apk
        :param tag_name: an optional tag to labeled the uploaded app.
        :param send_to_av_date: an optional date to delay sending apps to third party antivirus like Opswat.
        :return: Response object.
        """
        try:
            with open(app_path, "rb") as apk_file:
                file_name = path.basename(app_path)
                file_stream = apk_file.read()
                headers = {
                    Auth.FILE_HASH_HEADER_NAME: hashlib.sha1(file_stream).hexdigest()
                }
                response = self.http_post_file(
                    self.API_UPLOAD_URL,
                    headers,
                    file_stream,
                    file_name,
                    data={"tagName": tag_name,
                          "sendToAVDate": send_to_av_date})
        except IOError as e:
            logger.error(str(e), exc_info=True)
            response = None
        return response

    def get_engine_version(self, date=None, engine_id=None, lang=None):
        """Search an engine and its associated vulnerabilities.
        If no params return a list of all existing engines
        :param engine_id: engine id.
        :param date: search the engine available on that date.
        :param lang: output language of vulnerabilities fields.
        Values "es" or "en"
        :return: Response
        """
        url = self.API_ENGINE_VERSION_URL
        external_engine_version = EngineVersionRequest(date, engine_id,
                                                       lang)
        params = external_engine_version.get_encoded_params()
        if params:
            url = "{url}?{params}".format(url=self.API_ENGINE_VERSION_URL,
                                          params=params)
        return self.http_get(url)

    def upload_url(self, urls, tag_names=None):
        """Download apps from a market URLs
        :param urls:  List of urls to upload
        :param tag_names List of tags to identify the application
        :return: Response object
        """
        upload_data = UploadUrlRequest(urls, tag_names)
        return self.http_post(self.API_UPLOADURL_URL, headers=None,
                              body=upload_data.as_dict())

    def add_market_app(self, unique_origin_id, unique_version_id, platform,
                       origin, title, app_url, find_date, **extra_parameters):
        """Add app to Tacyt from a market.
        :param unique_origin_id: the unique id of the application in the market.
        :param unique_version_id: the unique version of the app in the market.
        :param platform: the platform of the application: iOS or Android.
        :param origin: the allowed market where the app is coming from.
        :param app_url: the url where the app can be found within market.
        :param title: the title to show in the market.
        :param find_date: date when the application was found in the market
        Usually the full application name.
        Example: applicationType should be application_type
        :param extra_parameters: a dictionary with extra parameters allowed by
        the api endpoint in snake_case.
        :return: Response object with the information created for the app.
        """
        external_market_app = NewMarketAppRequest(
            unique_origin_id=unique_origin_id,
            unique_version_id=unique_version_id,
            platform=platform,
            origin=origin,
            title=title,
            app_url=app_url,
            find_date=find_date,
            **extra_parameters)
        return self.http_post(self.API_MARKET_URL, headers=None,
                              body=external_market_app.as_dict())

    def update_market_app(self, unique_origin_id, unique_version_id, platform,
                          origin, title, app_url, find_date, **extra_parameters):
        """Update app to Tacyt from a market.
        :param unique_origin_id: the unique id of the application in the market.
        :param unique_version_id: the unique version of the app in the market.
        :param platform: the platform of the application: iOS or Android.
        :param origin: the allowed market where the app is coming from.
        :param app_url: the url where the app can be found within market.
        :param title: the title to show in the market.
        :param find_date: date when the application was found in the market
        Usually the full application name.
        Example: applicationType should be application_type
        :param extra_parameters: a dictionary with extra parameters allowed by
        the api endpoint in snake_case.
        :return: Response object with the latest information for the app.
        """
        external_market = UpdateMarketAppRequest(
            unique_origin_id=unique_origin_id,
            unique_version_id=unique_version_id,
            platform=platform,
            origin=origin,
            title=title,
            app_url=app_url,
            find_date=find_date,
            **extra_parameters)
        return self.http_put(self.API_MARKET_URL, headers=None,
                             body=external_market.as_dict())
