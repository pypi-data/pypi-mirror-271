# AbsenceReasonCategoryResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The Red Rover internal Id of AbsenceReasonCategory (numeric) | [optional] 
**external_id** | **str** | The external Id of AbsenceReason (alpha-numeric) | [optional] 
**name** | **str** | The Absence Reason Category&#39;s name | [optional] 
**description** | **str** | A detailed description of the Absence Reason Category | [optional] 
**valid_until_utc** | **datetime** | When the Absence Reason Category expires | [optional] 
**allow_negative_balance** | **bool** | If negative balances are allowed for this Absence Reason Categroy | [optional] 
**code** | **str** | The &#39;Code&#39; assigned to this Absence Reason Category. For external purposes | [optional] 
**balances_are_sensitive** | **bool** |  | [optional] 

## Example

```python
from redrover_api.models.absence_reason_category_response import AbsenceReasonCategoryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AbsenceReasonCategoryResponse from a JSON string
absence_reason_category_response_instance = AbsenceReasonCategoryResponse.from_json(json)
# print the JSON string representation of the object
print AbsenceReasonCategoryResponse.to_json()

# convert the object into a dict
absence_reason_category_response_dict = absence_reason_category_response_instance.to_dict()
# create an instance of AbsenceReasonCategoryResponse from a dict
absence_reason_category_response_form_dict = absence_reason_category_response.from_dict(absence_reason_category_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


