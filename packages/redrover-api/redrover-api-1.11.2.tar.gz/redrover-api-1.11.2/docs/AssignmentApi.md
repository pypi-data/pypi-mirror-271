# redrover_api.AssignmentApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_assignment**](AssignmentApi.md#get_assignment) | **GET** /api/v1/{orgId}/Assignment/{identifier} | Get Assignment


# **get_assignment**
> AssignmentResponse get_assignment(org_id, identifier)

Get Assignment

Get Assignment by Identifier

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.assignment_response import AssignmentResponse
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
    api_instance = redrover_api.AssignmentApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the Assignment. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)

    try:
        # Get Assignment
        api_response = api_instance.get_assignment(org_id, identifier)
        print("The response of AssignmentApi->get_assignment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AssignmentApi->get_assignment: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the Assignment. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

### Return type

[**AssignmentResponse**](AssignmentResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets Assignment |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. School Year not found. Employee not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

