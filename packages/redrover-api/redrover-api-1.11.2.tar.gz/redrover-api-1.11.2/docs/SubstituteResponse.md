# SubstituteResponse

SubstituteResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**List[SubstituteAttributeResponse]**](SubstituteAttributeResponse.md) | Attributes of the substitute | [optional] 
**related_org_ids** | **List[int]** | List of the OrganizationIds the user is related to | [optional] 
**pay_code** | [**PayCodeResponse**](PayCodeResponse.md) |  | [optional] 
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
from redrover_api.models.substitute_response import SubstituteResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SubstituteResponse from a JSON string
substitute_response_instance = SubstituteResponse.from_json(json)
# print the JSON string representation of the object
print SubstituteResponse.to_json()

# convert the object into a dict
substitute_response_dict = substitute_response_instance.to_dict()
# create an instance of SubstituteResponse from a dict
substitute_response_form_dict = substitute_response.from_dict(substitute_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


