# redrover_api.OrganizationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_current_school_years**](OrganizationApi.md#get_current_school_years) | **GET** /api/v1/Organization/{id}/schoolYear/current | Get current School Year
[**get_organization**](OrganizationApi.md#get_organization) | **GET** /api/v1/Organization/{id} | Get Organization
[**get_organizations**](OrganizationApi.md#get_organizations) | **GET** /api/v1/Organization | Get Organizations
[**get_school_years**](OrganizationApi.md#get_school_years) | **GET** /api/v1/Organization/{id}/schoolYear | Get School Years


# **get_current_school_years**
> SchoolYearResponse get_current_school_years(id)

Get current School Year

Get current School Year for an Organization

### Example

* Basic Authentication (basic):
```python
import time
import os
import redrover_api
from redrover_api.models.school_year_response import SchoolYearResponse
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
    api_instance = redrover_api.OrganizationApi(api_client)
    id = 56 # int | The Red Rover Id of the Organization

    try:
        # Get current School Year
        api_response = api_instance.get_current_school_years(id)
        print("The response of OrganizationApi->get_current_school_years:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->get_current_school_years: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The Red Rover Id of the Organization | 

### Return type

[**SchoolYearResponse**](SchoolYearResponse.md)

### Authorization

[basic](../README.md#basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns current School Year |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organization**
> OrganizationResponse get_organization(id)

Get Organization

Retrieve an organization you have been granted access to by its Id

### Example

* Basic Authentication (basic):
```python
import time
import os
import redrover_api
from redrover_api.models.organization_response import OrganizationResponse
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
    api_instance = redrover_api.OrganizationApi(api_client)
    id = 56 # int | The Red Rover Id of the Organization

    try:
        # Get Organization
        api_response = api_instance.get_organization(id)
        print("The response of OrganizationApi->get_organization:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->get_organization: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The Red Rover Id of the Organization | 

### Return type

[**OrganizationResponse**](OrganizationResponse.md)

### Authorization

[basic](../README.md#basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns Organization |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organizations**
> List[OrganizationResponse] get_organizations()

Get Organizations

Retrieve organizations you have been granted access to

### Example

* Basic Authentication (basic):
```python
import time
import os
import redrover_api
from redrover_api.models.organization_response import OrganizationResponse
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
    api_instance = redrover_api.OrganizationApi(api_client)

    try:
        # Get Organizations
        api_response = api_instance.get_organizations()
        print("The response of OrganizationApi->get_organizations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->get_organizations: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**List[OrganizationResponse]**](OrganizationResponse.md)

### Authorization

[basic](../README.md#basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns Organizations |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_school_years**
> List[SchoolYearResponse] get_school_years(id)

Get School Years

Get School Year data for an Organization

### Example

* Basic Authentication (basic):
```python
import time
import os
import redrover_api
from redrover_api.models.school_year_response import SchoolYearResponse
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
    api_instance = redrover_api.OrganizationApi(api_client)
    id = 56 # int | The Red Rover Id of the Organization

    try:
        # Get School Years
        api_response = api_instance.get_school_years(id)
        print("The response of OrganizationApi->get_school_years:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->get_school_years: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The Red Rover Id of the Organization | 

### Return type

[**List[SchoolYearResponse]**](SchoolYearResponse.md)

### Authorization

[basic](../README.md#basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns School Years |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

