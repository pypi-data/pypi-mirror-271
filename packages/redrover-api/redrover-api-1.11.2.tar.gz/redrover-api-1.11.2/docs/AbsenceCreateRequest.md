# AbsenceCreateRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**validate_only** | **bool** | When set, this will only validate the Absence and will not save it. (default: false) | [optional] [default to False]
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
from redrover_api.models.absence_create_request import AbsenceCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AbsenceCreateRequest from a JSON string
absence_create_request_instance = AbsenceCreateRequest.from_json(json)
# print the JSON string representation of the object
print AbsenceCreateRequest.to_json()

# convert the object into a dict
absence_create_request_dict = absence_create_request_instance.to_dict()
# create an instance of AbsenceCreateRequest from a dict
absence_create_request_form_dict = absence_create_request.from_dict(absence_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


