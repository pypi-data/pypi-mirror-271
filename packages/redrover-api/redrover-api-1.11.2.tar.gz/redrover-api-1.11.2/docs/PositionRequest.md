# PositionRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**external_id** | **str** | The external Id of SchoolYear (alpha-numeric) | [optional] 
**name** | **str** | The Position&#39;s name | [optional] 
**position_schedule_mode_id** | [**PositionScheduleModeEnum**](PositionScheduleModeEnum.md) |  | [optional] 
**contract** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | 
**position_type** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | 
**hours_per_full_work_day** | **float** | Amount of hours per a full workday (hours) | [optional] 
**needs_replacement** | [**NeedsReplacementEnum**](NeedsReplacementEnum.md) |  | [optional] 
**start_date** | **datetime** | The StartDate of the Position | [optional] 
**end_date** | **datetime** | The EndDate of the Position | [optional] 
**is_staff_augmentation** | **bool** | Is the Position for staff augmentation | [optional] [readonly] 
**fte** | **float** |  | [optional] 
**qualified_for_pto** | **bool** | Is the Position qualified for paid time off | [optional] 
**qualified_for_paid_holidays** | **bool** | Is the Position qualified for holidays | [optional] 
**qualified_for_pto_as_of** | **datetime** | The effective date that the Position qualifies for paid time off (If not included, the default is that it is always qualified) | [optional] 
**qualified_for_paid_holidays_as_of** | **datetime** | The effective date that the Position qualifies for holidays (If not included, the default is that it is always qualified) | [optional] 
**default_job_pay_override** | **float** |  | [optional] 
**code** | **str** | The &#39;Code&#39; for the Position. | [optional] 
**schedules** | [**List[PositionScheduleRequest]**](PositionScheduleRequest.md) | The Schedules for the Position | 
**replace_existing_position_jobs** | **bool** | If existing Position Jobs are to be replaced. (Default is true) | [optional] 
**allowed_location_ids** | [**List[Int32LocatorRequest]**](Int32LocatorRequest.md) | Locations the Position is granted | [optional] 
**other_jobs** | [**List[PositionJobRequest]**](PositionJobRequest.md) | Other Jobs | [optional] 
**primary_job** | [**PositionJobRequest**](PositionJobRequest.md) |  | [optional] 
**accounting_code_allocations** | [**List[AccountingCodeAllocationRequest]**](AccountingCodeAllocationRequest.md) | The Accounting Code Allocation for this position | [optional] 

## Example

```python
from redrover_api.models.position_request import PositionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PositionRequest from a JSON string
position_request_instance = PositionRequest.from_json(json)
# print the JSON string representation of the object
print PositionRequest.to_json()

# convert the object into a dict
position_request_dict = position_request_instance.to_dict()
# create an instance of PositionRequest from a dict
position_request_form_dict = position_request.from_dict(position_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


