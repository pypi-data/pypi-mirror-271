# AttributeResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The Red Rover internal Id of Attribute (numeric) | [optional] 
**name** | **str** | Name of the Attribute | [optional] 
**external_id** | **str** | The external Id of Attribute (alpha-numeric) | [optional] 
**active** | **bool** | If the Attribute is active | [optional] 
**description** | **str** | Description of the Attribute | [optional] 

## Example

```python
from redrover_api.models.attribute_response import AttributeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeResponse from a JSON string
attribute_response_instance = AttributeResponse.from_json(json)
# print the JSON string representation of the object
print AttributeResponse.to_json()

# convert the object into a dict
attribute_response_dict = attribute_response_instance.to_dict()
# create an instance of AttributeResponse from a dict
attribute_response_form_dict = attribute_response.from_dict(attribute_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


