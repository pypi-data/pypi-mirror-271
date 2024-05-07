# redrover_api.AbsenceReasonApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_absence_reason**](AbsenceReasonApi.md#get_absence_reason) | **GET** /api/v1/{orgId}/AbsenceReason/{identifier} | Get Absence Reason
[**get_absence_reasons**](AbsenceReasonApi.md#get_absence_reasons) | **GET** /api/v1/{orgId}/AbsenceReason | Get list of Absence Reasons


# **get_absence_reason**
> AbsenceReasonResponse get_absence_reason(org_id, identifier)

Get Absence Reason

Get a specific Absence Reason by it's identifier

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.absence_reason_response import AbsenceReasonResponse
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
    api_instance = redrover_api.AbsenceReasonApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the AbsenceReason. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)

    try:
        # Get Absence Reason
        api_response = api_instance.get_absence_reason(org_id, identifier)
        print("The response of AbsenceReasonApi->get_absence_reason:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AbsenceReasonApi->get_absence_reason: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the AbsenceReason. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

### Return type

[**AbsenceReasonResponse**](AbsenceReasonResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets Absence Reason |  -  |
**401** | Unauthorized |  -  |
**404** | AbsenceReason not found or has been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_absence_reasons**
> List[AbsenceReasonResponse] get_absence_reasons(org_id, identifiers)

Get list of Absence Reasons

Get a list of AbsenceReasons by their identifiers. Must use consistent Ids types (only Red Rover Ids, or ExternalIds).

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.absence_reason_response import AbsenceReasonResponse
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
    api_instance = redrover_api.AbsenceReasonApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifiers = ['identifiers_example'] # List[str] | The identifier of the AbsenceReasons. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)

    try:
        # Get list of Absence Reasons
        api_response = api_instance.get_absence_reasons(org_id, identifiers)
        print("The response of AbsenceReasonApi->get_absence_reasons:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AbsenceReasonApi->get_absence_reasons: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifiers** | [**List[str]**](str.md)| The identifier of the AbsenceReasons. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

### Return type

[**List[AbsenceReasonResponse]**](AbsenceReasonResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets Absence Reasons |  -  |
**401** | Unauthorized |  -  |
**404** | AbsenceReasons not found or has been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

