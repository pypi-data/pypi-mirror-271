# WebhookUpdateRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**webhook_uri** | **str** | The absolute uri that data will be posted to | 
**basic_auth_username** | **str** | The Basic Auth username. If this is included, the Webhook POST requests will contain a Base64-encoded header of &#39;BasicAuthUsername:BasicAuthPassword&#39;. (Optional) | [optional] 
**basic_auth_password** | **str** | The Basic Auth username. If this is included, the Webhook POST requests will contain a Base64-encoded header of &#39;BasicAuthUsername:BasicAuthPassword&#39;. (Optional) | [optional] 
**is_active** | **bool** | Whether this Webhook is active. If it is inactive, no data will be posted to it | [optional] 

## Example

```python
from redrover_api.models.webhook_update_request import WebhookUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookUpdateRequest from a JSON string
webhook_update_request_instance = WebhookUpdateRequest.from_json(json)
# print the JSON string representation of the object
print WebhookUpdateRequest.to_json()

# convert the object into a dict
webhook_update_request_dict = webhook_update_request_instance.to_dict()
# create an instance of WebhookUpdateRequest from a dict
webhook_update_request_form_dict = webhook_update_request.from_dict(webhook_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


