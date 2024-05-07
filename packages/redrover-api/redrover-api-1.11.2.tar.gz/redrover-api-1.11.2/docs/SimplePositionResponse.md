# SimplePositionResponse

Position

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | Name of the Position | [optional] [readonly] 
**position_type** | [**Int32IdNameClass**](Int32IdNameClass.md) |  | [optional] 
**name** | **str** |  | [optional] 
**id** | **int** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from redrover_api.models.simple_position_response import SimplePositionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SimplePositionResponse from a JSON string
simple_position_response_instance = SimplePositionResponse.from_json(json)
# print the JSON string representation of the object
print SimplePositionResponse.to_json()

# convert the object into a dict
simple_position_response_dict = simple_position_response_instance.to_dict()
# create an instance of SimplePositionResponse from a dict
simple_position_response_form_dict = simple_position_response.from_dict(simple_position_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


