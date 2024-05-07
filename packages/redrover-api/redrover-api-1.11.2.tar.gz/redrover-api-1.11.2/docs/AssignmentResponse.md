# AssignmentResponse

Assignment

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**employee** | [**Int32IdNameClass**](Int32IdNameClass.md) |  | [optional] 
**position** | [**Int32IdNameClass**](Int32IdNameClass.md) |  | [optional] 
**contract** | [**Int32IdNameClass**](Int32IdNameClass.md) |  | [optional] 
**vacancy** | [**VacancyResponse**](VacancyResponse.md) |  | [optional] 
**start_time_local** | **datetime** | When the Assignment starts (local time) | [optional] 
**end_time_local** | **datetime** | When the Assignment ends (local time) | [optional] 
**is_long_term** | **bool** | Is the Assignment classified as a long-term assignment | [optional] 
**cancelled_at_utc** | **datetime** | When was the Assignment cancelled | [optional] 
**id** | **int** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from redrover_api.models.assignment_response import AssignmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AssignmentResponse from a JSON string
assignment_response_instance = AssignmentResponse.from_json(json)
# print the JSON string representation of the object
print AssignmentResponse.to_json()

# convert the object into a dict
assignment_response_dict = assignment_response_instance.to_dict()
# create an instance of AssignmentResponse from a dict
assignment_response_form_dict = assignment_response.from_dict(assignment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


