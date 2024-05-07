# TimeOffBalanceRequest

TimeOffBalanceRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**absence_reason** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**absence_reason_category** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**school_year** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**as_of** | **datetime** | The &#39;AsOf&#39; date | [optional] 
**absence_reason_tracking_type_id** | [**AbsenceReasonTrackingTypeEnum**](AbsenceReasonTrackingTypeEnum.md) |  | [optional] 
**balance** | **float** | The balance for this time off balance request | [optional] 

## Example

```python
from redrover_api.models.time_off_balance_request import TimeOffBalanceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TimeOffBalanceRequest from a JSON string
time_off_balance_request_instance = TimeOffBalanceRequest.from_json(json)
# print the JSON string representation of the object
print TimeOffBalanceRequest.to_json()

# convert the object into a dict
time_off_balance_request_dict = time_off_balance_request_instance.to_dict()
# create an instance of TimeOffBalanceRequest from a dict
time_off_balance_request_form_dict = time_off_balance_request.from_dict(time_off_balance_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


