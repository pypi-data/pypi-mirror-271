# AbsenceReasonResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The Red Rover internal Id of AbsenceReason (numeric) | [optional] 
**external_id** | **str** | The external Id of AbsenceReason (alpha-numeric) | [optional] 
**allow_negative_balance** | **bool** | If negative balances are allowed for this Absence Reason | [optional] 
**name** | **str** | The Absence Reason&#39;s name | [optional] 
**description** | **str** | A detailed description of the Absence Reason | [optional] 
**category** | [**AbsenceReasonCategoryResponse**](AbsenceReasonCategoryResponse.md) |  | [optional] 
**requires_notes_to_admin** | **bool** | If this Absence Reason requires a note to the Administrator | [optional] 
**requires_approval** | **bool** | If this Absence Reason requires an approval | [optional] 
**code** | **str** | The &#39;Code&#39; assigned to this Absence Reason. For external purposes | [optional] 
**position_type_ids** | **List[int]** | Position Type Ids that are associated with this Absence Reason | [optional] 
**contract_ids** | **List[int]** | Contract Ids that are associated with this Absence Reason | [optional] 

## Example

```python
from redrover_api.models.absence_reason_response import AbsenceReasonResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AbsenceReasonResponse from a JSON string
absence_reason_response_instance = AbsenceReasonResponse.from_json(json)
# print the JSON string representation of the object
print AbsenceReasonResponse.to_json()

# convert the object into a dict
absence_reason_response_dict = absence_reason_response_instance.to_dict()
# create an instance of AbsenceReasonResponse from a dict
absence_reason_response_form_dict = absence_reason_response.from_dict(absence_reason_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


