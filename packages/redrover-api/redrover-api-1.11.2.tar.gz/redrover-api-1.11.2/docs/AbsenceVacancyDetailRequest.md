# AbsenceVacancyDetailRequest

The Vacancy Date Details

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**location** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**needs_replacement** | **bool** | If this Vacancy needs to be open for a Substitute to fill | [optional] 
**var_date** | **datetime** | The Date of this Detail | [optional] 
**day_part_id** | [**DayPartEnum**](DayPartEnum.md) |  | [optional] 
**start_time** | **str** | The time of day this Vacancy Detail begins | [optional] 
**end_time** | **str** | The time of day this Vacancy Detail ends | [optional] 
**accounting_code_allocations** | [**List[VacancyAccountingCodeAllocationRequest]**](VacancyAccountingCodeAllocationRequest.md) | Accounting code allocations | [optional] 
**pay_code** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**replacement_employee** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 

## Example

```python
from redrover_api.models.absence_vacancy_detail_request import AbsenceVacancyDetailRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AbsenceVacancyDetailRequest from a JSON string
absence_vacancy_detail_request_instance = AbsenceVacancyDetailRequest.from_json(json)
# print the JSON string representation of the object
print AbsenceVacancyDetailRequest.to_json()

# convert the object into a dict
absence_vacancy_detail_request_dict = absence_vacancy_detail_request_instance.to_dict()
# create an instance of AbsenceVacancyDetailRequest from a dict
absence_vacancy_detail_request_form_dict = absence_vacancy_detail_request.from_dict(absence_vacancy_detail_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


