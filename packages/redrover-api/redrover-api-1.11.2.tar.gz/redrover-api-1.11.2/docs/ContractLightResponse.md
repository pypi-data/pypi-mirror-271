# ContractLightResponse

Contract

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**id** | **int** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from redrover_api.models.contract_light_response import ContractLightResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ContractLightResponse from a JSON string
contract_light_response_instance = ContractLightResponse.from_json(json)
# print the JSON string representation of the object
print ContractLightResponse.to_json()

# convert the object into a dict
contract_light_response_dict = contract_light_response_instance.to_dict()
# create an instance of ContractLightResponse from a dict
contract_light_response_form_dict = contract_light_response.from_dict(contract_light_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


