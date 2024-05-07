# EmployeeResponse

Employee

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**positions** | [**List[PositionResponse]**](PositionResponse.md) | The Positions that belong to the employee | [optional] 
**id** | **int** | The Red Rover internal Id of OrgUser (numeric) | [optional] 
**org_id** | **int** | The Red Rover internal Id of Organization (numeric) | [optional] 
**created_utc** | **datetime** | When the User was created | [optional] 
**changed_utc** | **datetime** | When the User&#39;s record was last changed | [optional] 
**external_id** | **str** | The external Id of OrgUser (alpha-numeric) | [optional] 
**first_name** | **str** | The User&#39;s first name | [optional] 
**middle_name** | **str** | The User&#39;s middle name | [optional] 
**last_name** | **str** | The User&#39;s last name | [optional] 
**email** | **str** | The User&#39;s email | [optional] 
**notification_email** | **str** | The User&#39;s notification email (for SSO organizations only) | [optional] 
**login_email** | **str** | The User&#39;s Login email (for SSO organizations only) | [optional] 
**date_of_birth** | **datetime** | The User&#39;s date of birth | [optional] 
**address1** | **str** | The User&#39;s address | [optional] 
**address2** | **str** | The User&#39;s address (continued) | [optional] 
**city** | **str** | The User&#39;s city | [optional] 
**state** | [**StateEnum**](StateEnum.md) |  | [optional] 
**postal_code** | **str** | The User&#39;s postal code | [optional] 
**country** | [**CountryEnum**](CountryEnum.md) |  | [optional] 
**phone_number** | **str** | The User&#39;s phone number | [optional] 
**active** | **bool** | If the user is active | [optional] 
**permission_set_id** | **int** | The Red Rover internal Id of PermissionSet (numeric) | [optional] 
**is_deleted** | **bool** | Is the User Deleted | [optional] 

## Example

```python
from redrover_api.models.employee_response import EmployeeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of EmployeeResponse from a JSON string
employee_response_instance = EmployeeResponse.from_json(json)
# print the JSON string representation of the object
print EmployeeResponse.to_json()

# convert the object into a dict
employee_response_dict = employee_response_instance.to_dict()
# create an instance of EmployeeResponse from a dict
employee_response_form_dict = employee_response.from_dict(employee_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


