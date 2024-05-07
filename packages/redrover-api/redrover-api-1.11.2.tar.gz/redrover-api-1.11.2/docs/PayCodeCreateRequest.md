# PayCodeCreateRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the pay code | 
**description** | **str** | The pay code&#39;s description | 
**external_id** | **str** | The pay code&#39;s ExternalId | 
**expired** | **bool** | If the pay code is expired | 
**code** | **str** | The assigned code of the code | 
**hourly_rate** | **float** | The hourly rate | [optional] 
**unit_rate** | **float** | The unit rate | [optional] 
**half_day_rate** | **float** | The half date rate | [optional] 
**full_day_rate** | **float** | The full date rate | [optional] 

## Example

```python
from redrover_api.models.pay_code_create_request import PayCodeCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PayCodeCreateRequest from a JSON string
pay_code_create_request_instance = PayCodeCreateRequest.from_json(json)
# print the JSON string representation of the object
print PayCodeCreateRequest.to_json()

# convert the object into a dict
pay_code_create_request_dict = pay_code_create_request_instance.to_dict()
# create an instance of PayCodeCreateRequest from a dict
pay_code_create_request_form_dict = pay_code_create_request.from_dict(pay_code_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


