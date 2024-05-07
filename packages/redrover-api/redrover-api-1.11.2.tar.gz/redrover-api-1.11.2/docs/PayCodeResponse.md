# PayCodeResponse

The Pay code of the Vacancy

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | The Code used | [optional] 
**hourly_rate** | **float** | Hourly rate (decimal 7,2) | [optional] 
**unit_rate** | **float** | Unit rate (decimal 7,2) | [optional] 
**half_day_rate** | **float** | Half day rate (decimal 7,2) | [optional] 
**full_day_rate** | **float** | Full day rate (decimal 7,2) | [optional] 
**valid_until_utc** | **datetime** | When the pay code is valid until | [optional] 
**name** | **str** |  | [optional] 
**id** | **int** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from redrover_api.models.pay_code_response import PayCodeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PayCodeResponse from a JSON string
pay_code_response_instance = PayCodeResponse.from_json(json)
# print the JSON string representation of the object
print PayCodeResponse.to_json()

# convert the object into a dict
pay_code_response_dict = pay_code_response_instance.to_dict()
# create an instance of PayCodeResponse from a dict
pay_code_response_form_dict = pay_code_response.from_dict(pay_code_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


