# PositionJobRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**pay_step** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**override_pay_rate** | **float** | The pay rate override | [optional] 
**visible** | **bool** | If the Job is visible. (Default is true) | [optional] 
**position_job_id** | **int** | The Position Job Id | [optional] 
**effective_as_of** | **datetime** | The effective date of ths Job | [optional] 
**accounting_codes** | [**List[AccountingCodeAllocationRequest]**](AccountingCodeAllocationRequest.md) | Accounting code allocations | [optional] 

## Example

```python
from redrover_api.models.position_job_request import PositionJobRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PositionJobRequest from a JSON string
position_job_request_instance = PositionJobRequest.from_json(json)
# print the JSON string representation of the object
print PositionJobRequest.to_json()

# convert the object into a dict
position_job_request_dict = position_job_request_instance.to_dict()
# create an instance of PositionJobRequest from a dict
position_job_request_form_dict = position_job_request.from_dict(position_job_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


