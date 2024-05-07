# NotFoundResult


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status_code** | **int** |  | [optional] 

## Example

```python
from redrover_api.models.not_found_result import NotFoundResult

# TODO update the JSON string below
json = "{}"
# create an instance of NotFoundResult from a JSON string
not_found_result_instance = NotFoundResult.from_json(json)
# print the JSON string representation of the object
print NotFoundResult.to_json()

# convert the object into a dict
not_found_result_dict = not_found_result_instance.to_dict()
# create an instance of NotFoundResult from a dict
not_found_result_form_dict = not_found_result.from_dict(not_found_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


