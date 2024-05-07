# SubstituteAttributeResponse

SubstituteAttributeResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute** | [**Int32LocatorResponse**](Int32LocatorResponse.md) |  | [optional] 
**expires** | **datetime** | When the attribute expire | [optional] 

## Example

```python
from redrover_api.models.substitute_attribute_response import SubstituteAttributeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SubstituteAttributeResponse from a JSON string
substitute_attribute_response_instance = SubstituteAttributeResponse.from_json(json)
# print the JSON string representation of the object
print SubstituteAttributeResponse.to_json()

# convert the object into a dict
substitute_attribute_response_dict = substitute_attribute_response_instance.to_dict()
# create an instance of SubstituteAttributeResponse from a dict
substitute_attribute_response_form_dict = substitute_attribute_response.from_dict(substitute_attribute_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


