# AbsenceVacancyRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**position** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**details** | [**List[AbsenceVacancyDetailRequest]**](AbsenceVacancyDetailRequest.md) | The Details of the Vacancy | [optional] 
**notes_to_replacement** | **str** | Notes for the Replacement Substitute | [optional] 
**allow_sub_to_accept_part** | **bool** | Allows the Sub to accept individual parts of a Vacancy | [optional] 
**external_id** | **str** | The External Id of the Vacancy | [optional] 
**pay_code** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**hold_for_manual_fill** | **bool** | This will hold the Vacancy until it will be manually filled | [optional] 
**administrator_comments** | **str** | Administrator comments | [optional] 

## Example

```python
from redrover_api.models.absence_vacancy_request import AbsenceVacancyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AbsenceVacancyRequest from a JSON string
absence_vacancy_request_instance = AbsenceVacancyRequest.from_json(json)
# print the JSON string representation of the object
print AbsenceVacancyRequest.to_json()

# convert the object into a dict
absence_vacancy_request_dict = absence_vacancy_request_instance.to_dict()
# create an instance of AbsenceVacancyRequest from a dict
absence_vacancy_request_form_dict = absence_vacancy_request.from_dict(absence_vacancy_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


