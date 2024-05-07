# redrover_api.VacancyApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_vacancy**](VacancyApi.md#delete_vacancy) | **DELETE** /api/v1/{orgId}/Vacancy/{identifier} | Delete Vacancy By Id
[**get_vacancy**](VacancyApi.md#get_vacancy) | **GET** /api/v1/{orgId}/Vacancy/{identifier} | Get Vacancy By Id
[**get_vacancy_details**](VacancyApi.md#get_vacancy_details) | **GET** /api/v1/{orgId}/Vacancy/vacancyDetails |  Query Vacancy Details
[**post_vacancy**](VacancyApi.md#post_vacancy) | **POST** /api/v1/{orgId}/Vacancy | Create a Vacancy


# **delete_vacancy**
> OkResult delete_vacancy(org_id, identifier)

Delete Vacancy By Id

Delete specific Vacancy by it's identifier

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.ok_result import OkResult
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
    api_instance = redrover_api.VacancyApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the Vacancy. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)

    try:
        # Delete Vacancy By Id
        api_response = api_instance.delete_vacancy(org_id, identifier)
        print("The response of VacancyApi->delete_vacancy:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VacancyApi->delete_vacancy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the Vacancy. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

### Return type

[**OkResult**](OkResult.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Deletes the Vacancy |  -  |
**404** | Vacancy not found |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_vacancy**
> VacancyResponse get_vacancy(org_id, identifier)

Get Vacancy By Id

Get a specific Vacancy by it's identifier

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.vacancy_response import VacancyResponse
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
    api_instance = redrover_api.VacancyApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the Vacancy. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)

    try:
        # Get Vacancy By Id
        api_response = api_instance.get_vacancy(org_id, identifier)
        print("The response of VacancyApi->get_vacancy:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VacancyApi->get_vacancy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the Vacancy. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

### Return type

[**VacancyResponse**](VacancyResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets Vacancy |  -  |
**404** | Vacancy not found |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_vacancy_details**
> List[VacancyDetailSearchResponse] get_vacancy_details(org_id, from_date, to_date, api_key=api_key, verified=verified, filled=filled, substitute_source_org_id=substitute_source_org_id, limit=limit, offset=offset, include_deleted=include_deleted)

 Query Vacancy Details

Query for Vacancy Details based on specified search criteria

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.vacancy_detail_search_response import VacancyDetailSearchResponse
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
    api_instance = redrover_api.VacancyApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    from_date = '2013-10-20T19:20:30+01:00' # datetime | From date to filter Vacancies
    to_date = '2013-10-20T19:20:30+01:00' # datetime | From date to filter Vacancies
    api_key = 'api_key_example' # str |  (optional)
    verified = True # bool | If a Vacancy has been verified (optional)
    filled = True # bool | If a Vacancy has been filled (optional)
    substitute_source_org_id = 56 # int |  (optional)
    limit = 56 # int | Numerical limit of results returned (optional)
    offset = 0 # int | Offset of results returned (optional) (default to 0)
    include_deleted = False # bool |  (optional) (default to False)

    try:
        #  Query Vacancy Details
        api_response = api_instance.get_vacancy_details(org_id, from_date, to_date, api_key=api_key, verified=verified, filled=filled, substitute_source_org_id=substitute_source_org_id, limit=limit, offset=offset, include_deleted=include_deleted)
        print("The response of VacancyApi->get_vacancy_details:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VacancyApi->get_vacancy_details: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **from_date** | **datetime**| From date to filter Vacancies | 
 **to_date** | **datetime**| From date to filter Vacancies | 
 **api_key** | **str**|  | [optional] 
 **verified** | **bool**| If a Vacancy has been verified | [optional] 
 **filled** | **bool**| If a Vacancy has been filled | [optional] 
 **substitute_source_org_id** | **int**|  | [optional] 
 **limit** | **int**| Numerical limit of results returned | [optional] 
 **offset** | **int**| Offset of results returned | [optional] [default to 0]
 **include_deleted** | **bool**|  | [optional] [default to False]

### Return type

[**List[VacancyDetailSearchResponse]**](VacancyDetailSearchResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets Vacancy Details |  -  |
**400** | Limit may not be greater than 2500. FromDate may not be later than EndDate |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_vacancy**
> VacancyResponse post_vacancy(org_id, vacancy_create_request)

Create a Vacancy

Create a Vacancy

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.vacancy_create_request import VacancyCreateRequest
from redrover_api.models.vacancy_response import VacancyResponse
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
    api_instance = redrover_api.VacancyApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    vacancy_create_request = redrover_api.VacancyCreateRequest() # VacancyCreateRequest | The details of the Vacancy

    try:
        # Create a Vacancy
        api_response = api_instance.post_vacancy(org_id, vacancy_create_request)
        print("The response of VacancyApi->post_vacancy:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VacancyApi->post_vacancy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **vacancy_create_request** | [**VacancyCreateRequest**](VacancyCreateRequest.md)| The details of the Vacancy | 

### Return type

[**VacancyResponse**](VacancyResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Creates Vacancy |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

