# SimpleAbsenceDetail

Details of the Absence

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**absence_id** | **int** | Id of the Absence | [optional] 
**id** | **int** | Id of the Absence Detail | [optional] 
**absence_detail_id** | **int** | Id of the Absence Detail | [optional] 
**employee** | [**SimplePerson**](SimplePerson.md) |  | [optional] 
**start** | **datetime** | The StartDate of the Absence | [optional] 
**end** | **datetime** | The EndDate of the Absence | [optional] 
**reasons** | [**List[Reason]**](Reason.md) | The Absence Reasons | [optional] 

## Example

```python
from redrover_api.models.simple_absence_detail import SimpleAbsenceDetail

# TODO update the JSON string below
json = "{}"
# create an instance of SimpleAbsenceDetail from a JSON string
simple_absence_detail_instance = SimpleAbsenceDetail.from_json(json)
# print the JSON string representation of the object
print SimpleAbsenceDetail.to_json()

# convert the object into a dict
simple_absence_detail_dict = simple_absence_detail_instance.to_dict()
# create an instance of SimpleAbsenceDetail from a dict
simple_absence_detail_form_dict = simple_absence_detail.from_dict(simple_absence_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


