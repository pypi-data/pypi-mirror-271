# OrganizationResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**org_id** | **int** | The Red Rover internal id of the Organization | [optional] 
**name** | **str** | The Organization&#39;s name | [optional] 
**api_key** | **str** | The Api Key the Organization has granted you | [optional] 
**granted_at_utc** | **datetime** | When the Organization granted you | [optional] 

## Example

```python
from redrover_api.models.organization_response import OrganizationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of OrganizationResponse from a JSON string
organization_response_instance = OrganizationResponse.from_json(json)
# print the JSON string representation of the object
print OrganizationResponse.to_json()

# convert the object into a dict
organization_response_dict = organization_response_instance.to_dict()
# create an instance of OrganizationResponse from a dict
organization_response_form_dict = organization_response.from_dict(organization_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


