# AccountingCodeAllocationResponse

Accounting code allocations

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**accounting_code** | [**AccountingCodeLightResponse**](AccountingCodeLightResponse.md) |  | [optional] 
**allocation** | **float** | What percentage (decimal) the Accounting code is allocated to | [optional] 

## Example

```python
from redrover_api.models.accounting_code_allocation_response import AccountingCodeAllocationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AccountingCodeAllocationResponse from a JSON string
accounting_code_allocation_response_instance = AccountingCodeAllocationResponse.from_json(json)
# print the JSON string representation of the object
print AccountingCodeAllocationResponse.to_json()

# convert the object into a dict
accounting_code_allocation_response_dict = accounting_code_allocation_response_instance.to_dict()
# create an instance of AccountingCodeAllocationResponse from a dict
accounting_code_allocation_response_form_dict = accounting_code_allocation_response.from_dict(accounting_code_allocation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


