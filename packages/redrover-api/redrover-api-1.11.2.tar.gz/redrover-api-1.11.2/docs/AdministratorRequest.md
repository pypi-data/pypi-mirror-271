# AdministratorRequest

AdministratorRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access_control** | [**AccessControlRequest**](AccessControlRequest.md) |  | 
**replace_existing_related_orgs** | **bool** | If existing related Organizations will be replaced. (Default is true) | [optional] 
**is_super_user** | **bool** | If the Administrator is a super user | [optional] 
**related_org_ids** | **List[int]** | Organization Ids that the Administrator is related it | [optional] 
**id** | **int** | The Red Rover internal Id of OrgUser (numeric) | [optional] 
**secondary_identifier** | **str** | The secondary identifier for the User | [optional] 
**external_id** | **str** | The external Id of OrgUser (alpha-numeric) | [optional] 
**first_name** | **str** | The User&#39;s first name | [optional] 
**middle_name** | **str** | The User&#39;s middle name | [optional] 
**last_name** | **str** | The User&#39;s last name | [optional] 
**email** | **str** | The User&#39;s email (authentication) | [optional] 
**notification_email** | **str** | The User&#39;s email that will receive notifications. For SSO districts only. If empty, the Email field will be used. Field is optional | [optional] 
**date_of_birth** | **datetime** | The User&#39;s date of birth | [optional] 
**address1** | **str** | The User&#39;s address | [optional] 
**address2** | **str** | The User&#39;s address (continued) | [optional] 
**city** | **str** | The User&#39;s city | [optional] 
**postal_code** | **str** | The User&#39;s postal code | [optional] 
**badge_number** | **str** | The User&#39;s badge number | [optional] 
**state** | [**StateEnum**](StateEnum.md) |  | [optional] 
**country** | [**CountryEnum**](CountryEnum.md) |  | [optional] 
**phone_number** | **str** | The User&#39;s phone number | [optional] 
**active** | **bool** | If the user is active. (Default is true for Create) | [optional] 
**permission_set** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**remove_future_assignments_on_inactivate** | **bool** | If all assignments are to be removed if the user is inactivated at any time | [optional] 
**invite_immediately** | **bool** | If the user is to receive an invitation email right away | [optional] 

## Example

```python
from redrover_api.models.administrator_request import AdministratorRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AdministratorRequest from a JSON string
administrator_request_instance = AdministratorRequest.from_json(json)
# print the JSON string representation of the object
print AdministratorRequest.to_json()

# convert the object into a dict
administrator_request_dict = administrator_request_instance.to_dict()
# create an instance of AdministratorRequest from a dict
administrator_request_form_dict = administrator_request.from_dict(administrator_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


