# Int32LocatorRequest

The Identifiers of the object

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The Red Rover Id (numeric) | [optional] 
**external_id** | **str** | The External Id (alpha-numeric) | [optional] 

## Example

```python
from redrover_api.models.int32_locator_request import Int32LocatorRequest

# TODO update the JSON string below
json = "{}"
# create an instance of Int32LocatorRequest from a JSON string
int32_locator_request_instance = Int32LocatorRequest.from_json(json)
# print the JSON string representation of the object
print Int32LocatorRequest.to_json()

# convert the object into a dict
int32_locator_request_dict = int32_locator_request_instance.to_dict()
# create an instance of Int32LocatorRequest from a dict
int32_locator_request_form_dict = int32_locator_request.from_dict(int32_locator_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


