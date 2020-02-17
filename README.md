# TACYT PYTHON SDK
The tacyt sdk allow you to connect easier to the Tacyt API.

# Requirements and dependencies
* Python>2.7 or Python>3.6
* Read API documentation (https://tacyt.elevenpaths.com/help/api).
* To get the "API ID" and "Secret" (fundamental values for integrating Tacyt in any application) it’s necessary to have an account in Tacyt's website.

Pip should handle all your dependencies automatically.

The project uses:
- simplejson
- requests 


# Installation 
You can clone the repository and install it. 
git clone git@github.com:ElevenPaths/tacyt-sdk-python.git
pip install tacyt-sdk-python/ 

You can also get it directly with pip:
pip install git+git@github.com:ElevenPaths/tacyt-sdk-python.git#egg=tacytsdk
pip3 install  git+git@github.com:ElevenPaths/tacyt-sdk-python.git#egg=tacyt

# Methods Available


#### USING THE SDK IN PYTHON ####
* Install the sdk in an python environment.
* Create a TacytClient object with your credentials obtained from Tacyt's website.
```
from tacyt_sdk.client import TacytClient
tacyt_api =  TacytClient("APP_ID_HERE", "SECRET_KEY_HERE")
```
* Call to Tacyt Server to do searches, compare apps, list tags, create filters or get the RSS info ...
```
result_search = api.search_apps("title:\"5G Speed For Android\"")

list_app_key = ["com.linterna11GooglePlay", "com.sms.kat1aptoideapps"]
result_compare = api.compare_apps(list_app_key, "true")

result_tag = api.list_tags()

rule = filter.Filter.Rule('1', "contains(permissionName,\"SMS\")")
filter_structure = filter.Filter("Apps SMS Permissions", "Apps which has sms permissions", 1, filter.Filter.PUBLIC_VISIBILITY, rule)
result_filter = api.create_filter(filter_structure)

result_get_rss = api.get_RSS_info(filter_id)
```

* Each Tacyt's API call have a response data where you can check the errors and the data of the response. 
```
all_tags = api.list_tags()
all_tags.errors
all_tags.data 
```
