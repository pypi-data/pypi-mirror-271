# WebhookCreateRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**topic** | **str** | Webhook topics are structure like such &#x60;DOMAIN/ACTION&#x60;.   Supported domains are &#x60;absence&#x60;, &#x60;vacancy&#x60;, &#x60;substitute_assignment&#x60;.  Supported actions are &#x60;create&#x60;, &#x60;update&#x60;, &#x60;delete&#x60;. | 
**webhook_uri** | **str** | The absolute uri that data will be posted to | 
**basic_auth_username** | **str** | The Basic Auth username. If this is included, the Webhook POST requests will contain a Base64-encoded header of &#39;BasicAuthUsername:BasicAuthPassword&#39;. (Optional) | [optional] 
**basic_auth_password** | **str** | The Basic Auth username. If this is included, the Webhook POST requests will contain a Base64-encoded header of &#39;BasicAuthUsername:BasicAuthPassword&#39;. (Optional) | [optional] 
**is_active** | **bool** | Whether this Webhook is active. If it is inactive, no data will be posted to it | [optional] 

## Example

```python
from redrover_api.models.webhook_create_request import WebhookCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookCreateRequest from a JSON string
webhook_create_request_instance = WebhookCreateRequest.from_json(json)
# print the JSON string representation of the object
print WebhookCreateRequest.to_json()

# convert the object into a dict
webhook_create_request_dict = webhook_create_request_instance.to_dict()
# create an instance of WebhookCreateRequest from a dict
webhook_create_request_form_dict = webhook_create_request.from_dict(webhook_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


