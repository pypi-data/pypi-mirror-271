# SimplePosition

Position of the Employee

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | The name of the Position | [optional] 
**hours_per_full_work_day** | **float** | Hours per full work day | [optional] 
**position_type** | [**Int32IdNameClass**](Int32IdNameClass.md) |  | [optional] 
**needs_replacement** | [**NeedsReplacementEnum**](NeedsReplacementEnum.md) |  | [optional] 
**id** | **int** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from redrover_api.models.simple_position import SimplePosition

# TODO update the JSON string below
json = "{}"
# create an instance of SimplePosition from a JSON string
simple_position_instance = SimplePosition.from_json(json)
# print the JSON string representation of the object
print SimplePosition.to_json()

# convert the object into a dict
simple_position_dict = simple_position_instance.to_dict()
# create an instance of SimplePosition from a dict
simple_position_form_dict = simple_position.from_dict(simple_position_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


