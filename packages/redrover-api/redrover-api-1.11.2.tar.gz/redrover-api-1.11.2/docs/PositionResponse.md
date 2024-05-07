# PositionResponse

Position

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | The code of the position | [optional] 
**start_date** | **datetime** | The date the position begins | [optional] 
**end_date** | **datetime** | The date the position ends | [optional] 
**default_accounting_codes_from_schedule** | **bool** |  | [optional] 
**needs_replacement** | [**NeedsReplacementEnum**](NeedsReplacementEnum.md) |  | [optional] 
**contract** | [**ContractLightResponse**](ContractLightResponse.md) |  | [optional] 
**position_schedule_mode** | [**PositionScheduleModeEnum**](PositionScheduleModeEnum.md) |  | [optional] 
**hours_per_full_work_day** | **float** | The hours worked in a full day | [optional] 
**fte** | **float** |  | [optional] 
**qualified_for_pto_as_of** | **datetime** | When is the position qualified for PTO | [optional] 
**qualified_for_paid_holidays_as_of** | **datetime** | When is the position qualified for holidays | [optional] 

## Example

```python
from redrover_api.models.position_response import PositionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PositionResponse from a JSON string
position_response_instance = PositionResponse.from_json(json)
# print the JSON string representation of the object
print PositionResponse.to_json()

# convert the object into a dict
position_response_dict = position_response_instance.to_dict()
# create an instance of PositionResponse from a dict
position_response_form_dict = position_response.from_dict(position_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


