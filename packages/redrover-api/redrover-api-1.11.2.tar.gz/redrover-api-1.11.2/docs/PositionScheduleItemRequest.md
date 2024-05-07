# PositionScheduleItemRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**accounting_code_allocations** | [**List[AccountingCodeAllocationRequest]**](AccountingCodeAllocationRequest.md) | Accounting Code allocations | [optional] 
**location** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | 
**job** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**bell_schedule** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | 
**start_period** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**end_period** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**periods_not_needing_replacement** | [**List[Int32LocatorRequest]**](Int32LocatorRequest.md) | The Periods that do not need replacement | [optional] 
**standard_custom_schedule_variant** | [**PositionScheduleCustomVariantRequest**](PositionScheduleCustomVariantRequest.md) |  | [optional] 
**additional_custom_schedule_variants** | [**List[PositionScheduleCustomVariantRequest]**](PositionScheduleCustomVariantRequest.md) | Additional custom schedule variant | [optional] 

## Example

```python
from redrover_api.models.position_schedule_item_request import PositionScheduleItemRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PositionScheduleItemRequest from a JSON string
position_schedule_item_request_instance = PositionScheduleItemRequest.from_json(json)
# print the JSON string representation of the object
print PositionScheduleItemRequest.to_json()

# convert the object into a dict
position_schedule_item_request_dict = position_schedule_item_request_instance.to_dict()
# create an instance of PositionScheduleItemRequest from a dict
position_schedule_item_request_form_dict = position_schedule_item_request.from_dict(position_schedule_item_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


