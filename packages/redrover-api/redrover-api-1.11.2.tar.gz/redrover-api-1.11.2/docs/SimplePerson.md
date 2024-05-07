# SimplePerson

User

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Red Rover internal id of the user | [optional] 
**external_id** | **str** | External Id of the user | [optional] 
**secondary_identifier** | **str** | Secondary Identifier of the user | [optional] 
**first_name** | **str** | User&#39;s first name | [optional] 
**middle_name** | **str** | User&#39;s middle name | [optional] 
**last_name** | **str** | User&#39;s last name | [optional] 
**source_organization** | [**Int32IdNameClass**](Int32IdNameClass.md) |  | [optional] 

## Example

```python
from redrover_api.models.simple_person import SimplePerson

# TODO update the JSON string below
json = "{}"
# create an instance of SimplePerson from a JSON string
simple_person_instance = SimplePerson.from_json(json)
# print the JSON string representation of the object
print SimplePerson.to_json()

# convert the object into a dict
simple_person_dict = simple_person_instance.to_dict()
# create an instance of SimplePerson from a dict
simple_person_form_dict = simple_person.from_dict(simple_person_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


