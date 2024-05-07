# AbsenceResponse

Absence

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The Red Rover internal Id of Absence (numeric) | [optional] 
**external_id** | **str** | The external Id of Absence (alpha-numeric) | [optional] 
**org_id** | **int** | The Red Rover internal Id of Organization (numeric) | [optional] 
**start_time** | **datetime** | The first date of the Absence | [optional] 
**end_time** | **datetime** | The last date of the Absence | [optional] 
**number_of_days** | **int** | How many days the Absence spans | [optional] 
**is_closed** | **bool** | If the Absence is closed | [optional] 
**is_deleted** | **bool** | If the Absence is deleted | [optional] 
**approval_status** | **str** | The approval status of the Absence | [optional] 
**notes_to_approver** | **str** | Any notes that are meant to go to the person who will approve this Absence | [optional] 
**admin_only_notes** | **str** | Any notes that are entered by an admin for this Absence | [optional] 
**total_duration** | **float** | The total duration of this absence (minutes) | [optional] 
**total_day_portion** | **float** | The total duration of this absence (days) | [optional] 
**employee** | [**OrgUserEmployeeResponse**](OrgUserEmployeeResponse.md) |  | [optional] 
**absence_details** | [**List[AbsenceDetailResponse]**](AbsenceDetailResponse.md) | The details of the Absence | [optional] 
**admin_edit_url** | **str** | The Url that the Admin can edit the Absence | [optional] [readonly] 
**employee_edit_url** | **str** | The Url that the Employee can edit the Absence | [optional] [readonly] 
**vacancies** | [**List[VacancyResponse]**](VacancyResponse.md) | The Vacancies associated with this Absence | [optional] 

## Example

```python
from redrover_api.models.absence_response import AbsenceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AbsenceResponse from a JSON string
absence_response_instance = AbsenceResponse.from_json(json)
# print the JSON string representation of the object
print AbsenceResponse.to_json()

# convert the object into a dict
absence_response_dict = absence_response_instance.to_dict()
# create an instance of AbsenceResponse from a dict
absence_response_form_dict = absence_response.from_dict(absence_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


