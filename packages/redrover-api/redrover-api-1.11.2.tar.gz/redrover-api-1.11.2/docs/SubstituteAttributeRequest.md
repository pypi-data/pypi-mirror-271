# SubstituteAttributeRequest

SubstituteAttributeRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**expires** | **datetime** | When the attribute expires | [optional] 

## Example

```python
from redrover_api.models.substitute_attribute_request import SubstituteAttributeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SubstituteAttributeRequest from a JSON string
substitute_attribute_request_instance = SubstituteAttributeRequest.from_json(json)
# print the JSON string representation of the object
print SubstituteAttributeRequest.to_json()

# convert the object into a dict
substitute_attribute_request_dict = substitute_attribute_request_instance.to_dict()
# create an instance of SubstituteAttributeRequest from a dict
substitute_attribute_request_form_dict = substitute_attribute_request.from_dict(substitute_attribute_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


