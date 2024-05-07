# BadRequestResult


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status_code** | **int** |  | [optional] 

## Example

```python
from redrover_api.models.bad_request_result import BadRequestResult

# TODO update the JSON string below
json = "{}"
# create an instance of BadRequestResult from a JSON string
bad_request_result_instance = BadRequestResult.from_json(json)
# print the JSON string representation of the object
print BadRequestResult.to_json()

# convert the object into a dict
bad_request_result_dict = bad_request_result_instance.to_dict()
# create an instance of BadRequestResult from a dict
bad_request_result_form_dict = bad_request_result.from_dict(bad_request_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


