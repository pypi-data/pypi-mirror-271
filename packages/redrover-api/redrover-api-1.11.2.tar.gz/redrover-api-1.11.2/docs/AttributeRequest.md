# AttributeRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The Red Rover internal Id of Attribute (numeric) | [optional] 
**name** | **str** | The name of the Attribute | [optional] 
**external_id** | **str** | The external Id of Attribute (alpha-numeric) | [optional] 
**active** | **bool** | Whether the Attribute is active | [optional] 
**description** | **str** | The description of the Attribute | [optional] 

## Example

```python
from redrover_api.models.attribute_request import AttributeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeRequest from a JSON string
attribute_request_instance = AttributeRequest.from_json(json)
# print the JSON string representation of the object
print AttributeRequest.to_json()

# convert the object into a dict
attribute_request_dict = attribute_request_instance.to_dict()
# create an instance of AttributeRequest from a dict
attribute_request_form_dict = attribute_request.from_dict(attribute_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


