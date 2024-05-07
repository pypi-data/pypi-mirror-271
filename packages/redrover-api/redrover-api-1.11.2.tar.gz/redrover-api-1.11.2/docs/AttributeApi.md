# redrover_api.AttributeApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_attributes**](AttributeApi.md#create_attributes) | **POST** /api/v1/{orgId}/ReferenceData/attribute | Create attribute
[**gets_attributes**](AttributeApi.md#gets_attributes) | **GET** /api/v1/{orgId}/ReferenceData/attribute | Get Attributes


# **create_attributes**
> AttributeResponse create_attributes(org_id, api_key=api_key, attribute_request=attribute_request)

Create attribute

Create attributes for an Organization

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.attribute_request import AttributeRequest
from redrover_api.models.attribute_response import AttributeResponse
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
    api_instance = redrover_api.AttributeApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    api_key = 'api_key_example' # str |  (optional)
    attribute_request = redrover_api.AttributeRequest() # AttributeRequest |  (optional)

    try:
        # Create attribute
        api_response = api_instance.create_attributes(org_id, api_key=api_key, attribute_request=attribute_request)
        print("The response of AttributeApi->create_attributes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AttributeApi->create_attributes: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **api_key** | **str**|  | [optional] 
 **attribute_request** | [**AttributeRequest**](AttributeRequest.md)|  | [optional] 

### Return type

[**AttributeResponse**](AttributeResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully created attribute |  -  |
**401** | Unauthorized |  -  |
**412** | Client Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **gets_attributes**
> List[AttributeResponse] gets_attributes(org_id, api_key=api_key)

Get Attributes

Get Attributes for an Organization

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.attribute_response import AttributeResponse
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
    api_instance = redrover_api.AttributeApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    api_key = 'api_key_example' # str |  (optional)

    try:
        # Get Attributes
        api_response = api_instance.gets_attributes(org_id, api_key=api_key)
        print("The response of AttributeApi->gets_attributes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AttributeApi->gets_attributes: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **api_key** | **str**|  | [optional] 

### Return type

[**List[AttributeResponse]**](AttributeResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns Attribute |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

