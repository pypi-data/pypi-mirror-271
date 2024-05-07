# VacancyAccountingCodeAllocationRequest

Accounting Code Allocation

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**accounting_code** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | 
**allocation** | **float** | How much is to be allocated. (0-1.0) | 

## Example

```python
from redrover_api.models.vacancy_accounting_code_allocation_request import VacancyAccountingCodeAllocationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of VacancyAccountingCodeAllocationRequest from a JSON string
vacancy_accounting_code_allocation_request_instance = VacancyAccountingCodeAllocationRequest.from_json(json)
# print the JSON string representation of the object
print VacancyAccountingCodeAllocationRequest.to_json()

# convert the object into a dict
vacancy_accounting_code_allocation_request_dict = vacancy_accounting_code_allocation_request_instance.to_dict()
# create an instance of VacancyAccountingCodeAllocationRequest from a dict
vacancy_accounting_code_allocation_request_form_dict = vacancy_accounting_code_allocation_request.from_dict(vacancy_accounting_code_allocation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


