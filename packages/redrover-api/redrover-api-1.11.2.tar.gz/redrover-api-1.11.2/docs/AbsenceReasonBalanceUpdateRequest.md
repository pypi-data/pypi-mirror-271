# AbsenceReasonBalanceUpdateRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**initial_balance** | **float** | The starting balance for this Absence Reason | [optional] 
**balance_as_of** | **datetime** | The &#39;As of&#39; date as to when this balance was last update | [optional] 
**absence_reason_tracking_type** | [**AbsenceReasonTrackingTypeEnum**](AbsenceReasonTrackingTypeEnum.md) |  | [optional] 

## Example

```python
from redrover_api.models.absence_reason_balance_update_request import AbsenceReasonBalanceUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AbsenceReasonBalanceUpdateRequest from a JSON string
absence_reason_balance_update_request_instance = AbsenceReasonBalanceUpdateRequest.from_json(json)
# print the JSON string representation of the object
print AbsenceReasonBalanceUpdateRequest.to_json()

# convert the object into a dict
absence_reason_balance_update_request_dict = absence_reason_balance_update_request_instance.to_dict()
# create an instance of AbsenceReasonBalanceUpdateRequest from a dict
absence_reason_balance_update_request_form_dict = absence_reason_balance_update_request.from_dict(absence_reason_balance_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


