# AccessControlResponse

Access control levels of the user

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**all_locations** | **bool** | If the user has access to all locations | [optional] 
**all_position_types** | **bool** | If the user has access to all position types | [optional] 
**location_ids** | **List[int]** | The Ids of the Locations the user has access to | [optional] 
**location_group_ids** | **List[int]** | The Ids of the Location Groups the user has access to | [optional] 
**position_type_ids** | **List[int]** | The Ids of the Position Types the user has access to | [optional] 

## Example

```python
from redrover_api.models.access_control_response import AccessControlResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AccessControlResponse from a JSON string
access_control_response_instance = AccessControlResponse.from_json(json)
# print the JSON string representation of the object
print AccessControlResponse.to_json()

# convert the object into a dict
access_control_response_dict = access_control_response_instance.to_dict()
# create an instance of AccessControlResponse from a dict
access_control_response_form_dict = access_control_response.from_dict(access_control_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


