# Django application with User and ActivityPeriod models, write a custom management command to populate the database with some dummy data, and design an API to serve that data in the json format given above.



## Show Members

> To get all Members details.
```
GET   localhost:8000/api/v1/show/members
```
> To get spefic Member details.
```
GET   localhost:8000/api/v1/show/member/{id}
```


## Add Member

> To add a new Member to the database. The ID is required other values can be Updated in the Update Section.
```
POST   localhost:8000/api/v1/add/member

Content-Type:application/json;charset=UTF-8
{
  "id" : "id",
  "real_name" : "name",
  "tz" : "timeZone",
}
```


## Add Activity Period

> To add the Activity Period to the specific member.
```
POST   localhost:8000/api/v1/add/activity_period/{id}

Content-Type:application/json;charset=UTF-8
{
  "start_time" : "Mar 1 2020 11:11AM",
  "end_time" : "Mar 1 2020 2:00PM",
}
```


## Update Member

> To Update a specific Member. If the key which you are trying to update is not available then key value pair is inserted as a new record.
```
PUT   localhost:8000/api/v1/update/member/{id}

Content-Type:application/json;charset=UTF-8
{
  "key1" : "value1",
  "key2" : "value2",
  "key3" : "value3",
  ........
  "keyN" : "valueN",
}
```


## Delete Member

> To delete a Member from the database. The specified ID will be deleted from the Database.
```
DELETE   localhost:8000/api/v1/delete/member/{id}
```
