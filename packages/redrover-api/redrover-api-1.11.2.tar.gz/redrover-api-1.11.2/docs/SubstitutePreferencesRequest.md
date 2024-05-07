# SubstitutePreferencesRequest

SubstitutePreferencesRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**favorite_substitutes** | [**List[Int32LocatorRequest]**](Int32LocatorRequest.md) | Substitutes that are preferred favorites | [optional] 
**blocked_substitutes** | [**List[Int32LocatorRequest]**](Int32LocatorRequest.md) | Substitutes that are blocked | [optional] 
**auto_assigned_substitutes** | [**List[Int32LocatorRequest]**](Int32LocatorRequest.md) | Substitutes that can be auto assigned | [optional] 

## Example

```python
from redrover_api.models.substitute_preferences_request import SubstitutePreferencesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SubstitutePreferencesRequest from a JSON string
substitute_preferences_request_instance = SubstitutePreferencesRequest.from_json(json)
# print the JSON string representation of the object
print SubstitutePreferencesRequest.to_json()

# convert the object into a dict
substitute_preferences_request_dict = substitute_preferences_request_instance.to_dict()
# create an instance of SubstitutePreferencesRequest from a dict
substitute_preferences_request_form_dict = substitute_preferences_request.from_dict(substitute_preferences_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


