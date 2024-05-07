# redrover_api.ConnectionApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**download_report**](ConnectionApi.md#download_report) | **GET** /api/v1/{orgId}/Connection/{id}/download | Download Report
[**download_report_0**](ConnectionApi.md#download_report_0) | **POST** /api/v1/{orgId}/Connection/{id}/download | Download Report
[**post_report_data**](ConnectionApi.md#post_report_data) | **POST** /api/v1/{orgId}/Connection/{id}/data | Posts Report
[**run_report**](ConnectionApi.md#run_report) | **POST** /api/v1/{orgId}/Connection/{id}/run | Run Report


# **download_report**
> bytearray download_report(id, org_id, file_format=file_format, include_headers=include_headers, now_utc=now_utc, request_body=request_body)

Download Report

Download an existing report

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.file_format import FileFormat
from redrover_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = redrover_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: apiKey
configuration = redrover_api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with redrover_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = redrover_api.ConnectionApi(api_client)
    id = 56 # int | 
    org_id = 'org_id_example' # str | 
    file_format = redrover_api.FileFormat() # FileFormat | File format type. (Delimited, Flat) (optional)
    include_headers = True # bool | Whether to include headers on the report (optional)
    now_utc = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    request_body = ['request_body_example'] # List[str] |  (optional)

    try:
        # Download Report
        api_response = api_instance.download_report(id, org_id, file_format=file_format, include_headers=include_headers, now_utc=now_utc, request_body=request_body)
        print("The response of ConnectionApi->download_report:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionApi->download_report: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **org_id** | **str**|  | 
 **file_format** | [**FileFormat**](.md)| File format type. (Delimited, Flat) | [optional] 
 **include_headers** | **bool**| Whether to include headers on the report | [optional] 
 **now_utc** | **datetime**|  | [optional] 
 **request_body** | [**List[str]**](str.md)|  | [optional] 

### Return type

**bytearray**

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns file |  -  |
**401** | Unauthorized |  -  |
**403** | Not granted access to Connection |  -  |
**404** | Connection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_report_0**
> bytearray download_report_0(id, org_id, file_format=file_format, include_headers=include_headers, now_utc=now_utc, request_body=request_body)

Download Report

Download an existing report

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.file_format import FileFormat
from redrover_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = redrover_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: apiKey
configuration = redrover_api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with redrover_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = redrover_api.ConnectionApi(api_client)
    id = 56 # int | 
    org_id = 'org_id_example' # str | 
    file_format = redrover_api.FileFormat() # FileFormat | File format type. (Delimited, Flat) (optional)
    include_headers = True # bool | Whether to include headers on the report (optional)
    now_utc = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    request_body = ['request_body_example'] # List[str] |  (optional)

    try:
        # Download Report
        api_response = api_instance.download_report_0(id, org_id, file_format=file_format, include_headers=include_headers, now_utc=now_utc, request_body=request_body)
        print("The response of ConnectionApi->download_report_0:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionApi->download_report_0: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **org_id** | **str**|  | 
 **file_format** | [**FileFormat**](.md)| File format type. (Delimited, Flat) | [optional] 
 **include_headers** | **bool**| Whether to include headers on the report | [optional] 
 **now_utc** | **datetime**|  | [optional] 
 **request_body** | [**List[str]**](str.md)|  | [optional] 

### Return type

**bytearray**

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns file |  -  |
**401** | Unauthorized |  -  |
**403** | Not granted access to Connection |  -  |
**404** | Connection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_report_data**
> post_report_data(id, pascal_case, org_id, accept=accept, now_utc=now_utc, request_body=request_body)

Posts Report

Supply the date filter as the request body in the following JSON string array format.  (The content type for the body should be “application/json”.) For e.g. (`[\"Date BETWEEN '2020-07-01' AND '2020-07-30'\"]`

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = redrover_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: apiKey
configuration = redrover_api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with redrover_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = redrover_api.ConnectionApi(api_client)
    id = 56 # int | 
    pascal_case = False # bool | Pascal Case results (default to False)
    org_id = 'org_id_example' # str | 
    accept = 'application/json' # str |  (optional) (default to 'application/json')
    now_utc = '2013-10-20T19:20:30+01:00' # datetime | The 'now' date (optional)
    request_body = ['request_body_example'] # List[str] |  (optional)

    try:
        # Posts Report
        api_instance.post_report_data(id, pascal_case, org_id, accept=accept, now_utc=now_utc, request_body=request_body)
    except Exception as e:
        print("Exception when calling ConnectionApi->post_report_data: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **pascal_case** | **bool**| Pascal Case results | [default to False]
 **org_id** | **str**|  | 
 **accept** | **str**|  | [optional] [default to &#39;application/json&#39;]
 **now_utc** | **datetime**| The &#39;now&#39; date | [optional] 
 **request_body** | [**List[str]**](str.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Connection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **run_report**
> bytearray run_report(id, org_id, now_utc=now_utc, request_body=request_body)

Run Report

Run a report and receive a file download

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = redrover_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: apiKey
configuration = redrover_api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with redrover_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = redrover_api.ConnectionApi(api_client)
    id = 56 # int | The Id of the Report that will be run
    org_id = 'org_id_example' # str | 
    now_utc = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    request_body = ['request_body_example'] # List[str] |  (optional)

    try:
        # Run Report
        api_response = api_instance.run_report(id, org_id, now_utc=now_utc, request_body=request_body)
        print("The response of ConnectionApi->run_report:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionApi->run_report: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The Id of the Report that will be run | 
 **org_id** | **str**|  | 
 **now_utc** | **datetime**|  | [optional] 
 **request_body** | [**List[str]**](str.md)|  | [optional] 

### Return type

**bytearray**

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**401** | Unauthorized |  -  |
**403** | Not granted access to Connection |  -  |
**404** | Connection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

