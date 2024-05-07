# redrover_api.PayCodeApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_pay_code**](PayCodeApi.md#create_pay_code) | **POST** /api/v1/{orgId}/PayCode | Create new pay code
[**delete_pay_code**](PayCodeApi.md#delete_pay_code) | **DELETE** /api/v1/{orgId}/PayCode/{identifier} | Delete an pay code
[**get_pay_code**](PayCodeApi.md#get_pay_code) | **GET** /api/v1/{orgId}/PayCode/{identifier} | Get PayCode
[**get_pay_codes**](PayCodeApi.md#get_pay_codes) | **GET** /api/v1/{orgId}/PayCode | Get all pay codes
[**update_pay_code**](PayCodeApi.md#update_pay_code) | **PUT** /api/v1/{orgId}/PayCode/{identifier} | Update existing pay code


# **create_pay_code**
> PayCodeResponse create_pay_code(org_id, pay_code_create_request)

Create new pay code

Create an pay code for an Employee

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.pay_code_create_request import PayCodeCreateRequest
from redrover_api.models.pay_code_response import PayCodeResponse
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
    api_instance = redrover_api.PayCodeApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    pay_code_create_request = redrover_api.PayCodeCreateRequest() # PayCodeCreateRequest | The details of the PayCode

    try:
        # Create new pay code
        api_response = api_instance.create_pay_code(org_id, pay_code_create_request)
        print("The response of PayCodeApi->create_pay_code:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PayCodeApi->create_pay_code: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **pay_code_create_request** | [**PayCodeCreateRequest**](PayCodeCreateRequest.md)| The details of the PayCode | 

### Return type

[**PayCodeResponse**](PayCodeResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | PayCode created |  -  |
**400** | PayCode already exists. Invalid input |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_pay_code**
> OkResult delete_pay_code(org_id, identifier)

Delete an pay code

Delete an existing pay code based on it's identifier

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
    api_instance = redrover_api.PayCodeApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the PayCode. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)

    try:
        # Delete an pay code
        api_response = api_instance.delete_pay_code(org_id, identifier)
        print("The response of PayCodeApi->delete_pay_code:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PayCodeApi->delete_pay_code: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the PayCode. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

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
**200** | Deletes the PayCode |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. PayCodes not found or has already been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pay_code**
> PayCodeResponse get_pay_code(org_id, identifier)

Get PayCode

Get a specific pay code by it's identifier.

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.pay_code_response import PayCodeResponse
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
    api_instance = redrover_api.PayCodeApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the PayCode. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)

    try:
        # Get PayCode
        api_response = api_instance.get_pay_code(org_id, identifier)
        print("The response of PayCodeApi->get_pay_code:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PayCodeApi->get_pay_code: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the PayCode. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

### Return type

[**PayCodeResponse**](PayCodeResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets PayCode |  -  |
**401** | Unauthorized |  -  |
**404** | PayCodes not found or has been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pay_codes**
> List[PayCodeResponse] get_pay_codes(org_id)

Get all pay codes

Get all pay codes in an Organization

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.pay_code_response import PayCodeResponse
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
    api_instance = redrover_api.PayCodeApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization

    try:
        # Get all pay codes
        api_response = api_instance.get_pay_codes(org_id)
        print("The response of PayCodeApi->get_pay_codes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PayCodeApi->get_pay_codes: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 

### Return type

[**List[PayCodeResponse]**](PayCodeResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets PayCodes |  -  |
**401** | Unauthorized |  -  |
**404** | PayCodes not found or has been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_pay_code**
> PayCodeResponse update_pay_code(org_id, identifier, pay_code_update_request)

Update existing pay code

Update details an already existing pay code.

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.pay_code_response import PayCodeResponse
from redrover_api.models.pay_code_update_request import PayCodeUpdateRequest
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
    api_instance = redrover_api.PayCodeApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the PayCode. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)
    pay_code_update_request = redrover_api.PayCodeUpdateRequest() # PayCodeUpdateRequest | The PayCode Payload

    try:
        # Update existing pay code
        api_response = api_instance.update_pay_code(org_id, identifier, pay_code_update_request)
        print("The response of PayCodeApi->update_pay_code:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PayCodeApi->update_pay_code: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the PayCode. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 
 **pay_code_update_request** | [**PayCodeUpdateRequest**](PayCodeUpdateRequest.md)| The PayCode Payload | 

### Return type

[**PayCodeResponse**](PayCodeResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | PayCode updated |  -  |
**201** | PayCode created if it previously did not exist |  -  |
**400** | PayCode already exists. Employee not included in request. Invalid input |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. Employee not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

