# redrover_api.AbsenceReasonBalanceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_absence_reason_balance**](AbsenceReasonBalanceApi.md#create_absence_reason_balance) | **POST** /api/v1/{orgId}/Employee/{employeeIdentifier}/absenceReasonBalances | Create Absence Reason Balance
[**delete_absence_reason_balance**](AbsenceReasonBalanceApi.md#delete_absence_reason_balance) | **DELETE** /api/v1/{orgId}/Employee/{employeeIdentifier}/absenceReasonBalances/{id} | Delete Absence Reason Balance
[**get_absence_reason_balance**](AbsenceReasonBalanceApi.md#get_absence_reason_balance) | **GET** /api/v1/{orgId}/Employee/{employeeIdentifier}/absenceReasonBalances/{id} | Get Absence Reason Balance
[**get_absence_reason_balances**](AbsenceReasonBalanceApi.md#get_absence_reason_balances) | **GET** /api/v1/{orgId}/Employee/{employeeIdentifier}/absenceReasonBalances | Get Absence Reason Balances
[**update_absence_reason_balance**](AbsenceReasonBalanceApi.md#update_absence_reason_balance) | **PUT** /api/v1/{orgId}/Employee/{employeeIdentifier}/absenceReasonBalances/{id} | Update Absence Reason Balance


# **create_absence_reason_balance**
> AbsenceReasonBalanceResponse create_absence_reason_balance(org_id, employee_identifier, absence_reason_balance_create_request=absence_reason_balance_create_request)

Create Absence Reason Balance

Create new Absence Reason Balance for an Employee

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.absence_reason_balance_create_request import AbsenceReasonBalanceCreateRequest
from redrover_api.models.absence_reason_balance_response import AbsenceReasonBalanceResponse
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
    api_instance = redrover_api.AbsenceReasonBalanceApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    employee_identifier = 'employee_identifier_example' # str | The identifier of the Employee. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)
    absence_reason_balance_create_request = redrover_api.AbsenceReasonBalanceCreateRequest() # AbsenceReasonBalanceCreateRequest |  (optional)

    try:
        # Create Absence Reason Balance
        api_response = api_instance.create_absence_reason_balance(org_id, employee_identifier, absence_reason_balance_create_request=absence_reason_balance_create_request)
        print("The response of AbsenceReasonBalanceApi->create_absence_reason_balance:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AbsenceReasonBalanceApi->create_absence_reason_balance: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **employee_identifier** | **str**| The identifier of the Employee. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 
 **absence_reason_balance_create_request** | [**AbsenceReasonBalanceCreateRequest**](AbsenceReasonBalanceCreateRequest.md)|  | [optional] 

### Return type

[**AbsenceReasonBalanceResponse**](AbsenceReasonBalanceResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Creates Absence Reason Balance |  -  |
**400** | Absence Reason Balance already exists |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. Absence Reason not found. Absence Reason Category not found. School Year not found. Employee not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_absence_reason_balance**
> OkObjectResult delete_absence_reason_balance(org_id, employee_identifier, id)

Delete Absence Reason Balance

Delete an Absence Reason Balance for an Employee by its Red Rover Id (numeric)

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.ok_object_result import OkObjectResult
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
    api_instance = redrover_api.AbsenceReasonBalanceApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    employee_identifier = 'employee_identifier_example' # str | The identifier of the Employee. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)
    id = 56 # int | The id of the AbsenceReasonBalance

    try:
        # Delete Absence Reason Balance
        api_response = api_instance.delete_absence_reason_balance(org_id, employee_identifier, id)
        print("The response of AbsenceReasonBalanceApi->delete_absence_reason_balance:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AbsenceReasonBalanceApi->delete_absence_reason_balance: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **employee_identifier** | **str**| The identifier of the Employee. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 
 **id** | **int**| The id of the AbsenceReasonBalance | 

### Return type

[**OkObjectResult**](OkObjectResult.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Deletes Absence Reason Balance |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. Employee not found. Absence Reason Balance not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_absence_reason_balance**
> AbsenceReasonBalanceResponse get_absence_reason_balance(org_id, employee_identifier, id)

Get Absence Reason Balance

Gets a specific Absence Reason Balance by its Red Rover Id  (numeric)

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.absence_reason_balance_response import AbsenceReasonBalanceResponse
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
    api_instance = redrover_api.AbsenceReasonBalanceApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    employee_identifier = 'employee_identifier_example' # str | The identifier of the Employee. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)
    id = 56 # int | The id of the AbsenceReasonBalance

    try:
        # Get Absence Reason Balance
        api_response = api_instance.get_absence_reason_balance(org_id, employee_identifier, id)
        print("The response of AbsenceReasonBalanceApi->get_absence_reason_balance:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AbsenceReasonBalanceApi->get_absence_reason_balance: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **employee_identifier** | **str**| The identifier of the Employee. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 
 **id** | **int**| The id of the AbsenceReasonBalance | 

### Return type

[**AbsenceReasonBalanceResponse**](AbsenceReasonBalanceResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets Absence Reason Balance |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. Absence Reason Balance not found. Employee not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_absence_reason_balances**
> List[AbsenceReasonBalanceResponse] get_absence_reason_balances(org_id, employee_identifier, school_year_id=school_year_id)

Get Absence Reason Balances

Get Absence Reason Balance for an employee

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.absence_reason_balance_response import AbsenceReasonBalanceResponse
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
    api_instance = redrover_api.AbsenceReasonBalanceApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    employee_identifier = 'employee_identifier_example' # str | The identifier of the Employee. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)
    school_year_id = 56 # int | Filter by school year (optional) (optional)

    try:
        # Get Absence Reason Balances
        api_response = api_instance.get_absence_reason_balances(org_id, employee_identifier, school_year_id=school_year_id)
        print("The response of AbsenceReasonBalanceApi->get_absence_reason_balances:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AbsenceReasonBalanceApi->get_absence_reason_balances: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **employee_identifier** | **str**| The identifier of the Employee. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 
 **school_year_id** | **int**| Filter by school year (optional) | [optional] 

### Return type

[**List[AbsenceReasonBalanceResponse]**](AbsenceReasonBalanceResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets Absence Reason Balances |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. School Year not found. Employee not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_absence_reason_balance**
> AbsenceReasonBalanceResponse update_absence_reason_balance(org_id, employee_identifier, id, absence_reason_balance_update_request=absence_reason_balance_update_request)

Update Absence Reason Balance

Update an Absence Reason Balance for an Employee by its Red Rover Id (numeric)

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.absence_reason_balance_response import AbsenceReasonBalanceResponse
from redrover_api.models.absence_reason_balance_update_request import AbsenceReasonBalanceUpdateRequest
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
    api_instance = redrover_api.AbsenceReasonBalanceApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    employee_identifier = 'employee_identifier_example' # str | The identifier of the Employee. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)
    id = 56 # int | The id of the AbsenceReasonBalance
    absence_reason_balance_update_request = redrover_api.AbsenceReasonBalanceUpdateRequest() # AbsenceReasonBalanceUpdateRequest |  (optional)

    try:
        # Update Absence Reason Balance
        api_response = api_instance.update_absence_reason_balance(org_id, employee_identifier, id, absence_reason_balance_update_request=absence_reason_balance_update_request)
        print("The response of AbsenceReasonBalanceApi->update_absence_reason_balance:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AbsenceReasonBalanceApi->update_absence_reason_balance: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **employee_identifier** | **str**| The identifier of the Employee. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 
 **id** | **int**| The id of the AbsenceReasonBalance | 
 **absence_reason_balance_update_request** | [**AbsenceReasonBalanceUpdateRequest**](AbsenceReasonBalanceUpdateRequest.md)|  | [optional] 

### Return type

[**AbsenceReasonBalanceResponse**](AbsenceReasonBalanceResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updates Absence Reason Balance |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. Employee not found. Absence Reason Balance not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

