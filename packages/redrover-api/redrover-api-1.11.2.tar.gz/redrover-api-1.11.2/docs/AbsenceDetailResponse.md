# AbsenceDetailResponse

Absence Detail

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**date_part** | [**DayPartEnum**](DayPartEnum.md) |  | [optional] 
**start_time** | **datetime** | The start time of the Absence for this day | [optional] 
**end_time** | **datetime** | The end time of the Absence for this day | [optional] 
**absence_reason_usage** | [**List[AbsenceReasonUsageResponse]**](AbsenceReasonUsageResponse.md) | The usage of Absence Reasons for this day | [optional] 

## Example

```python
from redrover_api.models.absence_detail_response import AbsenceDetailResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AbsenceDetailResponse from a JSON string
absence_detail_response_instance = AbsenceDetailResponse.from_json(json)
# print the JSON string representation of the object
print AbsenceDetailResponse.to_json()

# convert the object into a dict
absence_detail_response_dict = absence_detail_response_instance.to_dict()
# create an instance of AbsenceDetailResponse from a dict
absence_detail_response_form_dict = absence_detail_response.from_dict(absence_detail_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


