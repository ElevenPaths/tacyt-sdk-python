### TACYT PYTHON SDK ###


#### PREREQUISITES ####

* Python.

* Read API documentation (https://path5.elevenpaths.com/help/api).

* To get the "API ID" and "Secret" (fundamental values for integrating Tacyt in any application) it’s necessary to have an account in Tacyt's website.

* In order to use the upload method you need the Python request library (http://docs.python-requests.org/en/latest/user/install/#install)


#### USING THE SDK IN PYTHON ####

* Include all SDK files and dependencies in your project.

* Create a TacytApp object with the "Application ID" and "Secret" previously obtained.
```
	api = tacytapp.TacytApp("APP_ID_HERE", "SECRET_KEY_HERE")
```

* Call to Tacyt Server to do searches, compare apps, list tags, create filters or get the RSS info ...
```
result_search = api.search_apps({"title":"5G Speed For Android"})

list_app_key = ["com.linterna11GooglePlay", "com.sms.kat1aptoideapps"]
result_compare = api.compare_apps(list_app_key, "true")

result_tag = api.list_tags()

rule = filter.Filter.Rule('1', "contains(permissionName,\"SMS\")")
filter_structure = filter.Filter("Apps SMS Permissions", "Apps which has sms permissions", 1, filter.Filter.PUBLIC_VISIBILITY, rule)
result_filter = api.create_filter(filter_structure)

result_get_rss = api.get_RSS_info(filter_id)
```

* After every API call, get Tacyt response data and errors and handle them.
```
	response_data = response.get_data()
	response_error = response.get_error()
  ```
