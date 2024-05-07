# Int32LocatorResponse

The Identifiers of the object

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The Red Rover Id (numeric) | [optional] 
**external_id** | **str** | The External Id (alpha-numeric) | [optional] 

## Example

```python
from redrover_api.models.int32_locator_response import Int32LocatorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of Int32LocatorResponse from a JSON string
int32_locator_response_instance = Int32LocatorResponse.from_json(json)
# print the JSON string representation of the object
print Int32LocatorResponse.to_json()

# convert the object into a dict
int32_locator_response_dict = int32_locator_response_instance.to_dict()
# create an instance of Int32LocatorResponse from a dict
int32_locator_response_form_dict = int32_locator_response.from_dict(int32_locator_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


