# AbsenceReasonBalanceCreateRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**school_year** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | 
**absence_reason** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | 
**absence_reason_category** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**initial_balance** | **float** | The starting balance for this Absence Reason | [optional] 
**balance_as_of** | **datetime** | The &#39;As of&#39; date as to when this balance was last update | [optional] 
**absence_reason_tracking_type** | [**AbsenceReasonTrackingTypeEnum**](AbsenceReasonTrackingTypeEnum.md) |  | [optional] 

## Example

```python
from redrover_api.models.absence_reason_balance_create_request import AbsenceReasonBalanceCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AbsenceReasonBalanceCreateRequest from a JSON string
absence_reason_balance_create_request_instance = AbsenceReasonBalanceCreateRequest.from_json(json)
# print the JSON string representation of the object
print AbsenceReasonBalanceCreateRequest.to_json()

# convert the object into a dict
absence_reason_balance_create_request_dict = absence_reason_balance_create_request_instance.to_dict()
# create an instance of AbsenceReasonBalanceCreateRequest from a dict
absence_reason_balance_create_request_form_dict = absence_reason_balance_create_request.from_dict(absence_reason_balance_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


