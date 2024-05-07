# AuthenticationProperties


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | **Dict[str, str]** |  | [optional] 
**parameters** | **Dict[str, object]** |  | [optional] 
**is_persistent** | **bool** |  | [optional] 
**redirect_uri** | **str** |  | [optional] 
**issued_utc** | **datetime** |  | [optional] 
**expires_utc** | **datetime** |  | [optional] 
**allow_refresh** | **bool** |  | [optional] 

## Example

```python
from redrover_api.models.authentication_properties import AuthenticationProperties

# TODO update the JSON string below
json = "{}"
# create an instance of AuthenticationProperties from a JSON string
authentication_properties_instance = AuthenticationProperties.from_json(json)
# print the JSON string representation of the object
print AuthenticationProperties.to_json()

# convert the object into a dict
authentication_properties_dict = authentication_properties_instance.to_dict()
# create an instance of AuthenticationProperties from a dict
authentication_properties_form_dict = authentication_properties.from_dict(authentication_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


