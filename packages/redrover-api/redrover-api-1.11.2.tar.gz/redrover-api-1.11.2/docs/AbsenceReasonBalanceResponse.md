# AbsenceReasonBalanceResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The Red Rover internal Id of AbsenceReasonBalance (numeric) | [optional] 
**employee_id** | **int** | The Red Rover internal Id of Employee (numeric) | [optional] 
**school_year_id** | **int** | The Red Rover internal Id of SchoolYear (numeric) | [optional] 
**absence_reason_id** | **int** | The Red Rover internal Id of AbsenceReason (numeric) | [optional] 
**absence_reason_category_id** | **int** | The Red Rover internal Id of AbsenceReasonCategory (numeric) | [optional] 
**balance_as_of** | **datetime** | The &#39;As of&#39; date as to when this balance was last update | [optional] 
**initial_balance** | **float** | How much the employee initially had | [optional] 
**used_balance** | **float** | How much has been used | [optional] 
**unused_balance** | **float** | How much has not been used | [optional] 
**earned_balance** | **float** | The amount of balance that was earned | [optional] 
**net_balance** | **float** | The net balance | [optional] 
**used_balance_calculated_at_utc** | **datetime** | When the last time that the &#39;used&#39; balance was calculated | [optional] 
**absence_reason_tracking_type** | [**AbsenceReasonTrackingTypeEnum**](AbsenceReasonTrackingTypeEnum.md) |  | [optional] 

## Example

```python
from redrover_api.models.absence_reason_balance_response import AbsenceReasonBalanceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AbsenceReasonBalanceResponse from a JSON string
absence_reason_balance_response_instance = AbsenceReasonBalanceResponse.from_json(json)
# print the JSON string representation of the object
print AbsenceReasonBalanceResponse.to_json()

# convert the object into a dict
absence_reason_balance_response_dict = absence_reason_balance_response_instance.to_dict()
# create an instance of AbsenceReasonBalanceResponse from a dict
absence_reason_balance_response_form_dict = absence_reason_balance_response.from_dict(absence_reason_balance_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


