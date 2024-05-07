# VacancyResponse

Vacancy

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**position** | [**SimplePositionResponse**](SimplePositionResponse.md) |  | [optional] 
**contract** | [**Int32IdNameClass**](Int32IdNameClass.md) |  | [optional] 
**approval_status** | [**ApprovalStatusEnum**](ApprovalStatusEnum.md) |  | [optional] 
**is_long_term** | **bool** | If the Vacancy is long term | [optional] 
**notes_to_replacement** | **str** | Notes to the Substitute | [optional] 
**admin_only_notes** | **str** | Notes for only Admins | [optional] 
**administrator_comments** | **str** | Administrator comments | [optional] 
**allow_sub_to_accept_part** | **bool** | If the Vacancy can be accepted in parts | [optional] 
**details** | [**List[VacancyDetailResponse]**](VacancyDetailResponse.md) | The Vacancy&#39;s Details | [optional] 
**hold_for_manual_fill_until_utc** | **datetime** | When the Vacancy is held for manual fill | [optional] 
**hold_for_auto_assign_until_utc** | **datetime** | When the Vacancy is held for auto assign | [optional] 
**fill_status** | [**FillStatusEnum**](FillStatusEnum.md) |  | [optional] 
**absence_id** | **int** | The Vacancy&#39;s AbsenceId if it is correlated to one | [optional] 
**admin_edit_url** | **str** | The Url that the Admin can edit the Vacancy or Absence that it is associated with | [optional] [readonly] 
**id** | **int** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from redrover_api.models.vacancy_response import VacancyResponse

# TODO update the JSON string below
json = "{}"
# create an instance of VacancyResponse from a JSON string
vacancy_response_instance = VacancyResponse.from_json(json)
# print the JSON string representation of the object
print VacancyResponse.to_json()

# convert the object into a dict
vacancy_response_dict = vacancy_response_instance.to_dict()
# create an instance of VacancyResponse from a dict
vacancy_response_form_dict = vacancy_response.from_dict(vacancy_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


