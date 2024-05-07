# OkObjectResult


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **object** |  | [optional] 
**formatters** | **List[object]** |  | [optional] 
**content_types** | **List[str]** |  | [optional] 
**declared_type** | **str** |  | [optional] 
**status_code** | **int** |  | [optional] 

## Example

```python
from redrover_api.models.ok_object_result import OkObjectResult

# TODO update the JSON string below
json = "{}"
# create an instance of OkObjectResult from a JSON string
ok_object_result_instance = OkObjectResult.from_json(json)
# print the JSON string representation of the object
print OkObjectResult.to_json()

# convert the object into a dict
ok_object_result_dict = ok_object_result_instance.to_dict()
# create an instance of OkObjectResult from a dict
ok_object_result_form_dict = ok_object_result.from_dict(ok_object_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


