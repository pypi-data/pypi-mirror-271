# SubstituteRelatedOrgRequest

SubstituteRelatedOrgRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**org_id** | **int** | The Red Rover internal Id of Organization (numeric) | [optional] 
**pay_code** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**attributes** | [**List[SubstituteAttributeRequest]**](SubstituteAttributeRequest.md) | The Substitute&#39;s attributes | [optional] 

## Example

```python
from redrover_api.models.substitute_related_org_request import SubstituteRelatedOrgRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SubstituteRelatedOrgRequest from a JSON string
substitute_related_org_request_instance = SubstituteRelatedOrgRequest.from_json(json)
# print the JSON string representation of the object
print SubstituteRelatedOrgRequest.to_json()

# convert the object into a dict
substitute_related_org_request_dict = substitute_related_org_request_instance.to_dict()
# create an instance of SubstituteRelatedOrgRequest from a dict
substitute_related_org_request_form_dict = substitute_related_org_request.from_dict(substitute_related_org_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


