# AbsenceUpdateRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**external_id** | **str** | The external identifier to the Absence | [optional] 
**employee** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**notes_to_approver** | **str** | Notes that will be shown to the individual who approves the Absence | [optional] 
**admin_only_notes** | **str** | Notes that will be only shown to Admins | [optional] 
**details** | [**List[AbsenceDetailCreateRequest]**](AbsenceDetailCreateRequest.md) | The specific details of the Absence | [optional] 
**start_date** | **datetime** | The date that the absence begins | [optional] 
**end_date** | **datetime** | The date that the absence ends | [optional] 
**vacancies** | [**List[AbsenceVacancyRequest]**](AbsenceVacancyRequest.md) | Assign a substitute to the Absence | [optional] 

## Example

```python
from redrover_api.models.absence_update_request import AbsenceUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AbsenceUpdateRequest from a JSON string
absence_update_request_instance = AbsenceUpdateRequest.from_json(json)
# print the JSON string representation of the object
print AbsenceUpdateRequest.to_json()

# convert the object into a dict
absence_update_request_dict = absence_update_request_instance.to_dict()
# create an instance of AbsenceUpdateRequest from a dict
absence_update_request_form_dict = absence_update_request.from_dict(absence_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


