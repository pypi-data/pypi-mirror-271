# AbsenceDetailCreateRequest

Absences are broken up into individual components called AbsenceDetails. Each AbsenceDetail is contained within one date. An absence can have many AbsenceDetails associated with it

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_date** | **datetime** | The Date of the AbsenceDetail | 
**day_part** | [**DayPartEnum**](DayPartEnum.md) |  | 
**description** | **str** |  | [optional] 
**start_time** | **datetime** | The start time of the AbsenceDetail | 
**end_time** | **datetime** | The start time of the AbsenceDetail | 
**reasons** | [**List[AbsenceReasonUsageCreateRequest]**](AbsenceReasonUsageCreateRequest.md) | The Reasons for absence in this AbsenceDetail | 

## Example

```python
from redrover_api.models.absence_detail_create_request import AbsenceDetailCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AbsenceDetailCreateRequest from a JSON string
absence_detail_create_request_instance = AbsenceDetailCreateRequest.from_json(json)
# print the JSON string representation of the object
print AbsenceDetailCreateRequest.to_json()

# convert the object into a dict
absence_detail_create_request_dict = absence_detail_create_request_instance.to_dict()
# create an instance of AbsenceDetailCreateRequest from a dict
absence_detail_create_request_form_dict = absence_detail_create_request.from_dict(absence_detail_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


