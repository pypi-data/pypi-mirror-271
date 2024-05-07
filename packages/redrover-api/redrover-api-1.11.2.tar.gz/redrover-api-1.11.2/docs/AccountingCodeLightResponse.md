# AccountingCodeLightResponse

The Accounting code that is associated with the Vacancy

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Red Rover internal id of the Accounting code | [optional] 
**code** | **str** | The Code used | [optional] 
**name** | **str** | The name of the Accounting code | [optional] 

## Example

```python
from redrover_api.models.accounting_code_light_response import AccountingCodeLightResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AccountingCodeLightResponse from a JSON string
accounting_code_light_response_instance = AccountingCodeLightResponse.from_json(json)
# print the JSON string representation of the object
print AccountingCodeLightResponse.to_json()

# convert the object into a dict
accounting_code_light_response_dict = accounting_code_light_response_instance.to_dict()
# create an instance of AccountingCodeLightResponse from a dict
accounting_code_light_response_form_dict = accounting_code_light_response.from_dict(accounting_code_light_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


