# WebhookResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**webhook_uri** | **str** | The absolute uri that data will be posted to | [optional] 
**id** | **str** | The Id of the Webhook (Guid) | [optional] 
**version** | **str** | The version of the webhook | [optional] 
**created** | **datetime** | When the webhook was created | [optional] 
**updated** | **datetime** | When the webhook was last updated | [optional] 
**topic** | **str** | Webhook topics are structure like such &#x60;DOMAIN/ACTION&#x60;.   Supported domains are &#x60;absence&#x60;, &#x60;vacancy&#x60;, &#x60;substitute_assignment&#x60;.  Supported actions are &#x60;create&#x60;, &#x60;update&#x60;, &#x60;delete&#x60;. | [optional] 
**basic_auth_username** | **str** | The Basic Auth username for the Basic Auth header that will be included in the Webhook payload | [optional] 
**basic_auth_password** | **str** | The Basic Auth password for the Basic Auth header that will be included in the Webhook payload | [optional] 
**is_active** | **bool** | If the Webhook is active | [optional] 

## Example

```python
from redrover_api.models.webhook_response import WebhookResponse

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookResponse from a JSON string
webhook_response_instance = WebhookResponse.from_json(json)
# print the JSON string representation of the object
print WebhookResponse.to_json()

# convert the object into a dict
webhook_response_dict = webhook_response_instance.to_dict()
# create an instance of WebhookResponse from a dict
webhook_response_form_dict = webhook_response.from_dict(webhook_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


