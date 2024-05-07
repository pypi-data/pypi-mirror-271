# AccountingCodeAllocationRequest

AccountingCodeAllocationRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**accounting_code_id** | **int** | The Red Rover internal Id of AccountingCode (numeric) | 
**allocation** | **float** | How much of the Accounting Code is allocated. Must be in decimal format (e.g. 0.4) | 

## Example

```python
from redrover_api.models.accounting_code_allocation_request import AccountingCodeAllocationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AccountingCodeAllocationRequest from a JSON string
accounting_code_allocation_request_instance = AccountingCodeAllocationRequest.from_json(json)
# print the JSON string representation of the object
print AccountingCodeAllocationRequest.to_json()

# convert the object into a dict
accounting_code_allocation_request_dict = accounting_code_allocation_request_instance.to_dict()
# create an instance of AccountingCodeAllocationRequest from a dict
accounting_code_allocation_request_form_dict = accounting_code_allocation_request.from_dict(accounting_code_allocation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


