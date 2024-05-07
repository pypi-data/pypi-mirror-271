# PositionScheduleRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[PositionScheduleItemRequest]**](PositionScheduleItemRequest.md) | Position Schedule Items | 
**days_of_the_week** | [**List[DayOfWeek]**](DayOfWeek.md) | Days of the week | 

## Example

```python
from redrover_api.models.position_schedule_request import PositionScheduleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PositionScheduleRequest from a JSON string
position_schedule_request_instance = PositionScheduleRequest.from_json(json)
# print the JSON string representation of the object
print PositionScheduleRequest.to_json()

# convert the object into a dict
position_schedule_request_dict = position_schedule_request_instance.to_dict()
# create an instance of PositionScheduleRequest from a dict
position_schedule_request_form_dict = position_schedule_request.from_dict(position_schedule_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


