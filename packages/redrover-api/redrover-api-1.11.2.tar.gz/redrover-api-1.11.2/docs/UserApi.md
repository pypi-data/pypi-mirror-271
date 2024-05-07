# redrover_api.UserApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_admin**](UserApi.md#create_admin) | **POST** /api/v1/{orgId}/User/administrator | Creates Administrator
[**create_employee**](UserApi.md#create_employee) | **POST** /api/v1/{orgId}/User/employee | Creates Employee
[**create_substitute**](UserApi.md#create_substitute) | **POST** /api/v1/{orgId}/User/substitute | Creates Substitute
[**delete_user**](UserApi.md#delete_user) | **DELETE** /api/v1/{orgId}/User/{identifier} | Deletes User
[**delete_user_role**](UserApi.md#delete_user_role) | **DELETE** /api/v1/{orgId}/User/{identifier}/{role} | Deletes User&#39;s Role
[**get_admin**](UserApi.md#get_admin) | **GET** /api/v1/{orgId}/User/administrator/{identifier} | Gets Administrator
[**get_employee**](UserApi.md#get_employee) | **GET** /api/v1/{orgId}/User/employee/{identifier} | Gets Employee
[**get_substitute**](UserApi.md#get_substitute) | **GET** /api/v1/{orgId}/User/substitute/{identifier} | Get Substitute by Id
[**get_substitutes**](UserApi.md#get_substitutes) | **GET** /api/v1/{orgId}/User/substitute | Query for Substitutes
[**update_admin**](UserApi.md#update_admin) | **PUT** /api/v1/{orgId}/User/administrator/{identifier} | Updates Administrator
[**update_employee**](UserApi.md#update_employee) | **PUT** /api/v1/{orgId}/User/employee/{identifier} | Updates Employee
[**update_substitute**](UserApi.md#update_substitute) | **PUT** /api/v1/{orgId}/User/substitute/{identifier} | Updates Substitute


# **create_admin**
> AdministratorResponse create_admin(org_id, administrator_request=administrator_request)

Creates Administrator

Create an Administrator

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.administrator_request import AdministratorRequest
from redrover_api.models.administrator_response import AdministratorResponse
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
    api_instance = redrover_api.UserApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    administrator_request = redrover_api.AdministratorRequest() # AdministratorRequest |  (optional)

    try:
        # Creates Administrator
        api_response = api_instance.create_admin(org_id, administrator_request=administrator_request)
        print("The response of UserApi->create_admin:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->create_admin: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **administrator_request** | [**AdministratorRequest**](AdministratorRequest.md)|  | [optional] 

### Return type

[**AdministratorResponse**](AdministratorResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Created / Updated Administrator |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_employee**
> EmployeeResponse create_employee(org_id, employee_request=employee_request)

Creates Employee

Create an Employee

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.employee_request import EmployeeRequest
from redrover_api.models.employee_response import EmployeeResponse
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
    api_instance = redrover_api.UserApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    employee_request = redrover_api.EmployeeRequest() # EmployeeRequest |  (optional)

    try:
        # Creates Employee
        api_response = api_instance.create_employee(org_id, employee_request=employee_request)
        print("The response of UserApi->create_employee:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->create_employee: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **employee_request** | [**EmployeeRequest**](EmployeeRequest.md)|  | [optional] 

### Return type

[**EmployeeResponse**](EmployeeResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Created / Updated Employee |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_substitute**
> SubstituteResponse create_substitute(org_id, substitute_request=substitute_request)

Creates Substitute

Creates a Substitute

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.substitute_request import SubstituteRequest
from redrover_api.models.substitute_response import SubstituteResponse
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
    api_instance = redrover_api.UserApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    substitute_request = redrover_api.SubstituteRequest() # SubstituteRequest |  (optional)

    try:
        # Creates Substitute
        api_response = api_instance.create_substitute(org_id, substitute_request=substitute_request)
        print("The response of UserApi->create_substitute:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->create_substitute: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **substitute_request** | [**SubstituteRequest**](SubstituteRequest.md)|  | [optional] 

### Return type

[**SubstituteResponse**](SubstituteResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Substitute Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user**
> OkResult delete_user(identifier, org_id)

Deletes User

Delete a user by their Red Rover Id

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
    api_instance = redrover_api.UserApi(api_client)
    identifier = 'identifier_example' # str | 
    org_id = 56 # int | The Red Rover Id of the Organization

    try:
        # Deletes User
        api_response = api_instance.delete_user(identifier, org_id)
        print("The response of UserApi->delete_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->delete_user: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**|  | 
 **org_id** | **int**| The Red Rover Id of the Organization | 

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
**200** | User Deleted |  -  |
**404** | Organization not found. OrgUser not found or has already been deleted |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user_role**
> OkResult delete_user_role(identifier, role, org_id)

Deletes User's Role

Delete a user's role by their Red Rover Id

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.ok_result import OkResult
from redrover_api.models.user_roles import UserRoles
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
    api_instance = redrover_api.UserApi(api_client)
    identifier = 'identifier_example' # str | 
    role = redrover_api.UserRoles() # UserRoles | 
    org_id = 56 # int | The Red Rover Id of the Organization

    try:
        # Deletes User's Role
        api_response = api_instance.delete_user_role(identifier, role, org_id)
        print("The response of UserApi->delete_user_role:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->delete_user_role: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**|  | 
 **role** | [**UserRoles**](.md)|  | 
 **org_id** | **int**| The Red Rover Id of the Organization | 

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
**200** | User Role Deleted |  -  |
**404** | Organization not found. OrgUser not found or has already been deleted |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_admin**
> AdministratorResponse get_admin(identifier, org_id)

Gets Administrator

Get an Administrator by their Red Rover Id

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.administrator_response import AdministratorResponse
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
    api_instance = redrover_api.UserApi(api_client)
    identifier = 'identifier_example' # str | 
    org_id = 56 # int | The Red Rover Id of the Organization

    try:
        # Gets Administrator
        api_response = api_instance.get_admin(identifier, org_id)
        print("The response of UserApi->get_admin:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->get_admin: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**|  | 
 **org_id** | **int**| The Red Rover Id of the Organization | 

### Return type

[**AdministratorResponse**](AdministratorResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns Administrator |  -  |
**401** | Unauthorized |  -  |
**404** | Administrator not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_employee**
> EmployeeResponse get_employee(identifier, org_id)

Gets Employee

Get an Employee by their Red Rover Id

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.employee_response import EmployeeResponse
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
    api_instance = redrover_api.UserApi(api_client)
    identifier = 'identifier_example' # str | 
    org_id = 56 # int | The Red Rover Id of the Organization

    try:
        # Gets Employee
        api_response = api_instance.get_employee(identifier, org_id)
        print("The response of UserApi->get_employee:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->get_employee: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**|  | 
 **org_id** | **int**| The Red Rover Id of the Organization | 

### Return type

[**EmployeeResponse**](EmployeeResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns Employee |  -  |
**401** | Unauthorized |  -  |
**404** | Employee not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_substitute**
> SubstituteResponse get_substitute(identifier, org_id)

Get Substitute by Id

Get a Substitute by their Red Rover Id

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.substitute_response import SubstituteResponse
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
    api_instance = redrover_api.UserApi(api_client)
    identifier = 'identifier_example' # str | 
    org_id = 56 # int | The Red Rover Id of the Organization

    try:
        # Get Substitute by Id
        api_response = api_instance.get_substitute(identifier, org_id)
        print("The response of UserApi->get_substitute:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->get_substitute: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**|  | 
 **org_id** | **int**| The Red Rover Id of the Organization | 

### Return type

[**SubstituteResponse**](SubstituteResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns Substitute |  -  |
**401** | Unauthorized |  -  |
**404** | Employee not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_substitutes**
> List[SubstituteResponse] get_substitutes(org_id, active=active, has_related_to_org_ids_any=has_related_to_org_ids_any, has_attribute_external_ids_any=has_attribute_external_ids_any, limit=limit, offset=offset)

Query for Substitutes

Query for Substitutes based on search criteria

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.substitute_response import SubstituteResponse
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
    api_instance = redrover_api.UserApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    active = True # bool | If the Substitute is active (optional)
    has_related_to_org_ids_any = [56] # List[int] |  (optional)
    has_attribute_external_ids_any = ['has_attribute_external_ids_any_example'] # List[str] |  (optional)
    limit = 56 # int | Limit. For pagination purposes (optional)
    offset = 0 # int | Offset. For pagination purposes (optional) (default to 0)

    try:
        # Query for Substitutes
        api_response = api_instance.get_substitutes(org_id, active=active, has_related_to_org_ids_any=has_related_to_org_ids_any, has_attribute_external_ids_any=has_attribute_external_ids_any, limit=limit, offset=offset)
        print("The response of UserApi->get_substitutes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->get_substitutes: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **active** | **bool**| If the Substitute is active | [optional] 
 **has_related_to_org_ids_any** | [**List[int]**](int.md)|  | [optional] 
 **has_attribute_external_ids_any** | [**List[str]**](str.md)|  | [optional] 
 **limit** | **int**| Limit. For pagination purposes | [optional] 
 **offset** | **int**| Offset. For pagination purposes | [optional] [default to 0]

### Return type

[**List[SubstituteResponse]**](SubstituteResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns Substitutes |  -  |
**401** | Unauthorized |  -  |
**400** | Limit may not be greater than 1000 |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_admin**
> AdministratorResponse update_admin(org_id, identifier, administrator_request=administrator_request)

Updates Administrator

Update an Administrator

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.administrator_request import AdministratorRequest
from redrover_api.models.administrator_response import AdministratorResponse
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
    api_instance = redrover_api.UserApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the OrgUser. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)
    administrator_request = redrover_api.AdministratorRequest() # AdministratorRequest |  (optional)

    try:
        # Updates Administrator
        api_response = api_instance.update_admin(org_id, identifier, administrator_request=administrator_request)
        print("The response of UserApi->update_admin:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->update_admin: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the OrgUser. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 
 **administrator_request** | [**AdministratorRequest**](AdministratorRequest.md)|  | [optional] 

### Return type

[**AdministratorResponse**](AdministratorResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Created / Updated Administrator |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_employee**
> EmployeeResponse update_employee(org_id, identifier, employee_request=employee_request)

Updates Employee

Update an Employee

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.employee_request import EmployeeRequest
from redrover_api.models.employee_response import EmployeeResponse
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
    api_instance = redrover_api.UserApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the OrgUser. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)
    employee_request = redrover_api.EmployeeRequest() # EmployeeRequest |  (optional)

    try:
        # Updates Employee
        api_response = api_instance.update_employee(org_id, identifier, employee_request=employee_request)
        print("The response of UserApi->update_employee:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->update_employee: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the OrgUser. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 
 **employee_request** | [**EmployeeRequest**](EmployeeRequest.md)|  | [optional] 

### Return type

[**EmployeeResponse**](EmployeeResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Created / Updated Employee |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_substitute**
> SubstituteResponse update_substitute(org_id, identifier, substitute_request=substitute_request)

Updates Substitute

Update a Substitute

### Example

* Basic Authentication (apiKey):
```python
import time
import os
import redrover_api
from redrover_api.models.substitute_request import SubstituteRequest
from redrover_api.models.substitute_response import SubstituteResponse
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
    api_instance = redrover_api.UserApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the OrgUser. If this is an External Id, prepend the value with the pike character `|` (e.g. `|ABC123`)
    substitute_request = redrover_api.SubstituteRequest() # SubstituteRequest |  (optional)

    try:
        # Updates Substitute
        api_response = api_instance.update_substitute(org_id, identifier, substitute_request=substitute_request)
        print("The response of UserApi->update_substitute:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->update_substitute: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the OrgUser. If this is an External Id, prepend the value with the pike character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 
 **substitute_request** | [**SubstituteRequest**](SubstituteRequest.md)|  | [optional] 

### Return type

[**SubstituteResponse**](SubstituteResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Creates / Updates Substitute |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

