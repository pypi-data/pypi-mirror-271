# redrover_api.AbsenceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_absence**](AbsenceApi.md#create_absence) | **POST** /api/v1/{orgId}/Absence | Create new Absence
[**delete_absence**](AbsenceApi.md#delete_absence) | **DELETE** /api/v1/{orgId}/Absence/{identifier} | Delete an Absence
[**get_absence**](AbsenceApi.md#get_absence) | **GET** /api/v1/{orgId}/Absence/{identifier} | Get Absence
[**get_absences**](AbsenceApi.md#get_absences) | **GET** /api/v1/{orgId}/Absence | Get list of Absences
[**update_absence**](AbsenceApi.md#update_absence) | **PUT** /api/v1/{orgId}/Absence/{identifier} | Update existing Absence


# **create_absence**
> AbsenceResponse create_absence(org_id, absence_create_request)

Create new Absence

Create an Absence for an Employee

### Example

* Basic Authentication (basic):
```python
import time
import os
import redrover_api
from redrover_api.models.absence_create_request import AbsenceCreateRequest
from redrover_api.models.absence_response import AbsenceResponse
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

# Configure HTTP basic authorization: basic
configuration = redrover_api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with redrover_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = redrover_api.AbsenceApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    absence_create_request = redrover_api.AbsenceCreateRequest() # AbsenceCreateRequest | The details of the Absence

    try:
        # Create new Absence
        api_response = api_instance.create_absence(org_id, absence_create_request)
        print("The response of AbsenceApi->create_absence:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AbsenceApi->create_absence: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **absence_create_request** | [**AbsenceCreateRequest**](AbsenceCreateRequest.md)| The details of the Absence | 

### Return type

[**AbsenceResponse**](AbsenceResponse.md)

### Authorization

[basic](../README.md#basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Absence created |  -  |
**400** | Absence already exists. Invalid input |  -  |
**401** | Unauthorized |  -  |
**404** | Absences not found or has been deleted. Organization not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_absence**
> OkResult delete_absence(org_id, identifier)

Delete an Absence

Delete an existing Absence based on it's identifier

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
    api_instance = redrover_api.AbsenceApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the Absence. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)

    try:
        # Delete an Absence
        api_response = api_instance.delete_absence(org_id, identifier)
        print("The response of AbsenceApi->delete_absence:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AbsenceApi->delete_absence: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the Absence. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

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
**200** | Deletes the Absence |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. Absences not found or has already been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_absence**
> AbsenceResponse get_absence(org_id, identifier)

Get Absence

Get a specific Absence by it's identifier.

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.absence_response import AbsenceResponse
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
    api_instance = redrover_api.AbsenceApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the Absence. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)

    try:
        # Get Absence
        api_response = api_instance.get_absence(org_id, identifier)
        print("The response of AbsenceApi->get_absence:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AbsenceApi->get_absence: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the Absence. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

### Return type

[**AbsenceResponse**](AbsenceResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets Absence |  -  |
**401** | Unauthorized |  -  |
**404** | Absences not found or has been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_absences**
> List[AbsenceResponse] get_absences(org_id, identifiers)

Get list of Absences

Get a list of Absences by their identifiers. Must use consistent Ids types (only Red Rover Ids, or ExternalIds).

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.absence_response import AbsenceResponse
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
    api_instance = redrover_api.AbsenceApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifiers = ['identifiers_example'] # List[str] | The identifier of the Absences. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)

    try:
        # Get list of Absences
        api_response = api_instance.get_absences(org_id, identifiers)
        print("The response of AbsenceApi->get_absences:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AbsenceApi->get_absences: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifiers** | [**List[str]**](str.md)| The identifier of the Absences. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

### Return type

[**List[AbsenceResponse]**](AbsenceResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets Absences |  -  |
**401** | Unauthorized |  -  |
**404** | Absences not found or has been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_absence**
> AbsenceResponse update_absence(org_id, identifier, absence_update_request)

Update existing Absence

Update details an already existing Absence.

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.absence_response import AbsenceResponse
from redrover_api.models.absence_update_request import AbsenceUpdateRequest
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
    api_instance = redrover_api.AbsenceApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the Absence. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)
    absence_update_request = redrover_api.AbsenceUpdateRequest() # AbsenceUpdateRequest | The Absence Payload

    try:
        # Update existing Absence
        api_response = api_instance.update_absence(org_id, identifier, absence_update_request)
        print("The response of AbsenceApi->update_absence:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AbsenceApi->update_absence: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the Absence. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 
 **absence_update_request** | [**AbsenceUpdateRequest**](AbsenceUpdateRequest.md)| The Absence Payload | 

### Return type

[**AbsenceResponse**](AbsenceResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Absence updated |  -  |
**201** | Absence created if it previously did not exist |  -  |
**400** | Absence already exists. Employee not included in request. Invalid input |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. Employee not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

