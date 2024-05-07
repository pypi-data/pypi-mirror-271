# AbsenceReasonUsageResponse

Absence Reason Usage

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The Red Rover internal Id of AbsenceReasonUsage (numeric) | [optional] 
**external_id** | **str** | The external Id of AbsenceReasonUsage (alpha-numeric) | [optional] 
**absence_reason_id** | **int** | The Red Rover internal Id of AbsenceReason (numeric) | [optional] 
**daily_amount** | **float** | The allocation of this Absence Reason for this day (daily) | [optional] 
**hourly_amount** | **float** | The allocation of this Absence Reason for this day (hourly) | [optional] 
**absence_reason** | [**AbsenceReasonResponse**](AbsenceReasonResponse.md) |  | [optional] 

## Example

```python
from redrover_api.models.absence_reason_usage_response import AbsenceReasonUsageResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AbsenceReasonUsageResponse from a JSON string
absence_reason_usage_response_instance = AbsenceReasonUsageResponse.from_json(json)
# print the JSON string representation of the object
print AbsenceReasonUsageResponse.to_json()

# convert the object into a dict
absence_reason_usage_response_dict = absence_reason_usage_response_instance.to_dict()
# create an instance of AbsenceReasonUsageResponse from a dict
absence_reason_usage_response_form_dict = absence_reason_usage_response.from_dict(absence_reason_usage_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


