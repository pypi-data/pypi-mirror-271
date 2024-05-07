# PositionScheduleCustomVariantRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_time** | **str** | The start time | [optional] 
**half_day_morning_end_time** | **str** | Halfday morning start time | [optional] 
**half_day_afternoon_start_time** | **str** | Halfday afternoon start time | [optional] 
**end_time** | **str** | The next end time | [optional] 
**next_start_time** | **str** | The next start time | [optional] 
**is_work_time** | **bool** | If is work time | [optional] 
**needs_replacement** | **bool** | If needs replacement | [optional] 
**needs_replacement_am** | **bool** | If needs replacement for AM | [optional] 
**needs_replacement_pm** | **bool** | If needs replacement for PM | [optional] 
**work_day_schedule_variant_type** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 

## Example

```python
from redrover_api.models.position_schedule_custom_variant_request import PositionScheduleCustomVariantRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PositionScheduleCustomVariantRequest from a JSON string
position_schedule_custom_variant_request_instance = PositionScheduleCustomVariantRequest.from_json(json)
# print the JSON string representation of the object
print PositionScheduleCustomVariantRequest.to_json()

# convert the object into a dict
position_schedule_custom_variant_request_dict = position_schedule_custom_variant_request_instance.to_dict()
# create an instance of PositionScheduleCustomVariantRequest from a dict
position_schedule_custom_variant_request_form_dict = position_schedule_custom_variant_request.from_dict(position_schedule_custom_variant_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


