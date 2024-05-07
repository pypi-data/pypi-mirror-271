# ForbidResult


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**authentication_schemes** | **List[str]** |  | [optional] 
**properties** | [**AuthenticationProperties**](AuthenticationProperties.md) |  | [optional] 

## Example

```python
from redrover_api.models.forbid_result import ForbidResult

# TODO update the JSON string below
json = "{}"
# create an instance of ForbidResult from a JSON string
forbid_result_instance = ForbidResult.from_json(json)
# print the JSON string representation of the object
print ForbidResult.to_json()

# convert the object into a dict
forbid_result_dict = forbid_result_instance.to_dict()
# create an instance of ForbidResult from a dict
forbid_result_form_dict = forbid_result.from_dict(forbid_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


