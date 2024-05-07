# Reason

The Reason for the Absence

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**absence_reason_id** | **int** | Id of the Absence&#39;s Reason | [optional] 
**external_id** | **str** | The External Id for the Absence Reason | [optional] 
**name** | **str** | The Reason | [optional] 

## Example

```python
from redrover_api.models.reason import Reason

# TODO update the JSON string below
json = "{}"
# create an instance of Reason from a JSON string
reason_instance = Reason.from_json(json)
# print the JSON string representation of the object
print Reason.to_json()

# convert the object into a dict
reason_dict = reason_instance.to_dict()
# create an instance of Reason from a dict
reason_form_dict = reason.from_dict(reason_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


