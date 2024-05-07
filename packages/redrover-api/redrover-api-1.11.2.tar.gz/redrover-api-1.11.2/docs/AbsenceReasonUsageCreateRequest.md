# AbsenceReasonUsageCreateRequest

An AbsenceDetail can have multiple reasons for the absence. This property allocates the AbsenceReason(s) to the AbsenceDetail

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**usage** | **str** |  | [optional] 
**daily_amount** | **float** | What percentage (decimal value) of the Absence is used by this AbsenceReason. E.g. 0.5 | [optional] 
**hourly_amount** | **float** | How many hours (decimal value) of the Absence is used by this AbsenceReason. E.g. 3.5 | [optional] 
**id** | **int** | The Red Rover Id (numeric) | [optional] 
**external_id** | **str** | The External Id (alpha-numeric) | [optional] 

## Example

```python
from redrover_api.models.absence_reason_usage_create_request import AbsenceReasonUsageCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AbsenceReasonUsageCreateRequest from a JSON string
absence_reason_usage_create_request_instance = AbsenceReasonUsageCreateRequest.from_json(json)
# print the JSON string representation of the object
print AbsenceReasonUsageCreateRequest.to_json()

# convert the object into a dict
absence_reason_usage_create_request_dict = absence_reason_usage_create_request_instance.to_dict()
# create an instance of AbsenceReasonUsageCreateRequest from a dict
absence_reason_usage_create_request_form_dict = absence_reason_usage_create_request.from_dict(absence_reason_usage_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


