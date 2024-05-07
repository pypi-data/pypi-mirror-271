# redrover_api.WebhooksApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_webhook**](WebhooksApi.md#create_webhook) | **POST** /api/v1/Webhooks | Create Webhook.
[**delete_webhook**](WebhooksApi.md#delete_webhook) | **DELETE** /api/v1/Webhooks/{id} | Delete Webhook
[**get_webhook**](WebhooksApi.md#get_webhook) | **GET** /api/v1/Webhooks | Get Webhooks
[**get_webhook_0**](WebhooksApi.md#get_webhook_0) | **GET** /api/v1/Webhooks/{identifier} | Get Webhook
[**put_webhook_uri**](WebhooksApi.md#put_webhook_uri) | **PUT** /api/v1/Webhooks/{id} | Update Webhook


# **create_webhook**
> WebhookResponse create_webhook(webhook_create_request=webhook_create_request)

Create Webhook.

Create a new Webhook  The 'Topic' is the type of webhook that you are creating. Please use the following standard: **domain/action**  The supported domains are `absence`, `vacancy`, `substitute_assignment`, `administrator`, `employee`, `substitute`  The supported actions are `create`, `update`, `delete`

### Example

* Basic Authentication (basic):
```python
import time
import os
import redrover_api
from redrover_api.models.webhook_create_request import WebhookCreateRequest
from redrover_api.models.webhook_response import WebhookResponse
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
    api_instance = redrover_api.WebhooksApi(api_client)
    webhook_create_request = redrover_api.WebhookCreateRequest() # WebhookCreateRequest |  (optional)

    try:
        # Create Webhook.
        api_response = api_instance.create_webhook(webhook_create_request=webhook_create_request)
        print("The response of WebhooksApi->create_webhook:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->create_webhook: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **webhook_create_request** | [**WebhookCreateRequest**](WebhookCreateRequest.md)|  | [optional] 

### Return type

[**WebhookResponse**](WebhookResponse.md)

### Authorization

[basic](../README.md#basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Creates Webhook |  -  |
**400** | Webhook already exists for this topic |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_webhook**
> OkResult delete_webhook(id)

Delete Webhook

In doing this, this will make all of the User's implementation of this webhook disabled

### Example

* Basic Authentication (basic):
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

# Configure HTTP basic authorization: basic
configuration = redrover_api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with redrover_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = redrover_api.WebhooksApi(api_client)
    id = 'id_example' # str | The Id of the Webhook (Guid)

    try:
        # Delete Webhook
        api_response = api_instance.delete_webhook(id)
        print("The response of WebhooksApi->delete_webhook:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->delete_webhook: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The Id of the Webhook (Guid) | 

### Return type

[**OkResult**](OkResult.md)

### Authorization

[basic](../README.md#basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Webhook deleted |  -  |
**401** | Unauthorized |  -  |
**404** | Webhook not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_webhook**
> List[WebhookResponse] get_webhook()

Get Webhooks

Gets all of your Webhooks

### Example

* Basic Authentication (basic):
```python
import time
import os
import redrover_api
from redrover_api.models.webhook_response import WebhookResponse
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
    api_instance = redrover_api.WebhooksApi(api_client)

    try:
        # Get Webhooks
        api_response = api_instance.get_webhook()
        print("The response of WebhooksApi->get_webhook:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->get_webhook: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**List[WebhookResponse]**](WebhookResponse.md)

### Authorization

[basic](../README.md#basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns Webhooks |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_webhook_0**
> WebhookResponse get_webhook_0(identifier)

Get Webhook

Gets a specific Webhook by its Id (Guid)

### Example

* Basic Authentication (basic):
```python
import time
import os
import redrover_api
from redrover_api.models.webhook_response import WebhookResponse
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
    api_instance = redrover_api.WebhooksApi(api_client)
    identifier = 'identifier_example' # str | The Id of the Webhook. (Guid)

    try:
        # Get Webhook
        api_response = api_instance.get_webhook_0(identifier)
        print("The response of WebhooksApi->get_webhook_0:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->get_webhook_0: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| The Id of the Webhook. (Guid) | 

### Return type

[**WebhookResponse**](WebhookResponse.md)

### Authorization

[basic](../README.md#basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns Webhook |  -  |
**401** | Unauthorized |  -  |
**404** | Webhook not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_webhook_uri**
> WebhookResponse put_webhook_uri(id, webhook_update_request=webhook_update_request)

Update Webhook

Updates a Webhook's Uri, Basic Auth credentials, and whether it is Active. Additional documentation can be found in our help desk: https://help.redroverk12.com/hc/en-us/articles/4417040764308-Webhooks

### Example

* Basic Authentication (basic):
```python
import time
import os
import redrover_api
from redrover_api.models.webhook_response import WebhookResponse
from redrover_api.models.webhook_update_request import WebhookUpdateRequest
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
    api_instance = redrover_api.WebhooksApi(api_client)
    id = 'id_example' # str | The Id of the Webhook (Guid)
    webhook_update_request = redrover_api.WebhookUpdateRequest() # WebhookUpdateRequest |  (optional)

    try:
        # Update Webhook
        api_response = api_instance.put_webhook_uri(id, webhook_update_request=webhook_update_request)
        print("The response of WebhooksApi->put_webhook_uri:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->put_webhook_uri: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The Id of the Webhook (Guid) | 
 **webhook_update_request** | [**WebhookUpdateRequest**](WebhookUpdateRequest.md)|  | [optional] 

### Return type

[**WebhookResponse**](WebhookResponse.md)

### Authorization

[basic](../README.md#basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully updated Uri |  -  |
**400** | Invalid Uri |  -  |
**401** | Unauthorized |  -  |
**404** | Webhook not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

