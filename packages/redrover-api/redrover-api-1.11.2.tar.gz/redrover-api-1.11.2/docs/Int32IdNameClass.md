# Int32IdNameClass

Contains the Id, ExternalId, and Name

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**id** | **int** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from redrover_api.models.int32_id_name_class import Int32IdNameClass

# TODO update the JSON string below
json = "{}"
# create an instance of Int32IdNameClass from a JSON string
int32_id_name_class_instance = Int32IdNameClass.from_json(json)
# print the JSON string representation of the object
print Int32IdNameClass.to_json()

# convert the object into a dict
int32_id_name_class_dict = int32_id_name_class_instance.to_dict()
# create an instance of Int32IdNameClass from a dict
int32_id_name_class_form_dict = int32_id_name_class.from_dict(int32_id_name_class_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


