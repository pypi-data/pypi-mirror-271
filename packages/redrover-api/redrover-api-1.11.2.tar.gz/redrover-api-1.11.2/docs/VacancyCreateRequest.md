# VacancyCreateRequest

Vacancy Create Request

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**position_type** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**contract** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**details** | [**List[VacancyDetailCreateRequest]**](VacancyDetailCreateRequest.md) | The Details of the Vacancy | [optional] 
**location** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**bell_schedule** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**title** | **str** | The Title of the Position that will be created | [optional] 
**notes_to_replacement** | **str** | Notes for the Replacement Substitute | [optional] 
**allow_sub_to_accept_part** | **bool** | Allows the Sub to accept individual parts of a Vacancy | [optional] 
**external_id** | **str** | The External Id of the Vacancy | [optional] 
**pay_code** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**hold_for_manual_fill** | **bool** | This will hold the Vacancy until it will be manually filled | [optional] 
**administrator_comments** | **str** | Administrator comments | [optional] 

## Example

```python
from redrover_api.models.vacancy_create_request import VacancyCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of VacancyCreateRequest from a JSON string
vacancy_create_request_instance = VacancyCreateRequest.from_json(json)
# print the JSON string representation of the object
print VacancyCreateRequest.to_json()

# convert the object into a dict
vacancy_create_request_dict = vacancy_create_request_instance.to_dict()
# create an instance of VacancyCreateRequest from a dict
vacancy_create_request_form_dict = vacancy_create_request.from_dict(vacancy_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


