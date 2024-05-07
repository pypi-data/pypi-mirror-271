# VacancyDetailResponse

Vacancy Detail

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Id of the Vacancy Detail | [optional] 
**assignment_id** | **int** | Id of the Assignment | [optional] 
**substitute** | [**SimplePerson**](SimplePerson.md) |  | [optional] 
**external_assignment_number** | **str** | Assignment number to match another system | [optional] 
**assignment_is_long_term** | **bool** | Is this assignment considered long term? | [optional] 
**assignment_notes** | **str** | Notes about this assignment | [optional] 
**location** | [**Int32IdNameClass**](Int32IdNameClass.md) |  | [optional] 
**start** | **datetime** | When the Vacancy starts | [optional] 
**end** | **datetime** | When the Vacancy ends | [optional] 
**actual_duration_minutes** | **int** | How long the Vacancy Detail is scheduled (minutes) | [optional] 
**accounting_codes** | [**List[AccountingCodeAllocationResponse]**](AccountingCodeAllocationResponse.md) | The Accounting codes associated with the Vacancy | [optional] 
**pay_duration** | **float** | The Calculated Effective Duration (Days or Minutes) | [optional] 
**pay_unit** | **str** | The pay unit. (&#39;DAYS&#39;, &#39;MINUTES&#39;) | [optional] 
**pay_code** | [**PayCodeResponse**](PayCodeResponse.md) |  | [optional] 
**vacancy_reason** | [**Int32IdNameClass**](Int32IdNameClass.md) |  | [optional] 
**verified** | **bool** | If the Vacancy has been verified | [optional] 
**verified_at_utc** | **datetime** | When the Vacancy was verified | [optional] 
**verify_comment** | **str** | Comment made when the Vacancy was verified | [optional] 
**verified_by** | [**Int32IdNameClass**](Int32IdNameClass.md) |  | [optional] 
**approval_status** | **str** | The current approval status of the vacancy | [optional] 
**approval_status_id** | [**ApprovalStatusEnum**](ApprovalStatusEnum.md) |  | [optional] 

## Example

```python
from redrover_api.models.vacancy_detail_response import VacancyDetailResponse

# TODO update the JSON string below
json = "{}"
# create an instance of VacancyDetailResponse from a JSON string
vacancy_detail_response_instance = VacancyDetailResponse.from_json(json)
# print the JSON string representation of the object
print VacancyDetailResponse.to_json()

# convert the object into a dict
vacancy_detail_response_dict = vacancy_detail_response_instance.to_dict()
# create an instance of VacancyDetailResponse from a dict
vacancy_detail_response_form_dict = vacancy_detail_response.from_dict(vacancy_detail_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


