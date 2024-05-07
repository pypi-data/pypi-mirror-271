# AccessControlRequest

AccessControlRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**all_locations** | **bool** | If the Administrator can be granted access to all Locations | [optional] 
**all_position_types** | **bool** | If the Administrator can be granted access to all Position Types | [optional] 
**locations** | [**List[Int32LocatorRequest]**](Int32LocatorRequest.md) | The Locations that the Administrator is granted access to | [optional] 
**location_groups** | [**List[Int32LocatorRequest]**](Int32LocatorRequest.md) | The Location Groups that the Administrator is granted access to | [optional] 
**position_types** | [**List[Int32LocatorRequest]**](Int32LocatorRequest.md) | The Position Types that the Administrator is granted access to | [optional] 

## Example

```python
from redrover_api.models.access_control_request import AccessControlRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AccessControlRequest from a JSON string
access_control_request_instance = AccessControlRequest.from_json(json)
# print the JSON string representation of the object
print AccessControlRequest.to_json()

# convert the object into a dict
access_control_request_dict = access_control_request_instance.to_dict()
# create an instance of AccessControlRequest from a dict
access_control_request_form_dict = access_control_request.from_dict(access_control_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


