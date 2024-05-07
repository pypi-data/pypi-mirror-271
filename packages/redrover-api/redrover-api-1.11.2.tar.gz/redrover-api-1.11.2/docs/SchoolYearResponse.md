# SchoolYearResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The Red Rover internal Id of SchoolYear (numeric) | [optional] 
**name** | **str** | The generated name for the School Year | [optional] 
**start_date** | **datetime** | The Start Date of the School Year | [optional] 
**end_date** | **datetime** | The End Date of the School Year | [optional] 
**earliest_date_for_absence_entry** | **datetime** | The date in which Absences are allowed to be created | [optional] 
**is_current_school_year** | **bool** | Is this the current school year | [optional] 

## Example

```python
from redrover_api.models.school_year_response import SchoolYearResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SchoolYearResponse from a JSON string
school_year_response_instance = SchoolYearResponse.from_json(json)
# print the JSON string representation of the object
print SchoolYearResponse.to_json()

# convert the object into a dict
school_year_response_dict = school_year_response_instance.to_dict()
# create an instance of SchoolYearResponse from a dict
school_year_response_form_dict = school_year_response.from_dict(school_year_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


