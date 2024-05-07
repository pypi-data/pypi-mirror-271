# OrgUserEmployeeResponse

Employee

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The Red Rover internal Id of OrgUser (numeric) | [optional] 
**external_id** | **str** | The external Id of OrgUser (alpha-numeric) | [optional] 
**first_name** | **str** | User&#39;s first name | [optional] 
**last_name** | **str** | User&#39;s last name | [optional] 
**secondary_identifier** | **str** | Secondary Identifier of the user | [optional] 

## Example

```python
from redrover_api.models.org_user_employee_response import OrgUserEmployeeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of OrgUserEmployeeResponse from a JSON string
org_user_employee_response_instance = OrgUserEmployeeResponse.from_json(json)
# print the JSON string representation of the object
print OrgUserEmployeeResponse.to_json()

# convert the object into a dict
org_user_employee_response_dict = org_user_employee_response_instance.to_dict()
# create an instance of OrgUserEmployeeResponse from a dict
org_user_employee_response_form_dict = org_user_employee_response.from_dict(org_user_employee_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


