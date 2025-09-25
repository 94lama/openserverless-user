# Tasks

Write mock functions to simulate the following tasks:

- Implement the address web action to manage the database table of an user control panel using PostGres, and exposing a REST API;
- Create the database and a schema (using as static name the name of the action);
- Write unit and integration tests;
- Write the documentationof the API in the file docs/ADDRESS.md.


# Specifications:

## Schema

Describes the schema structure of the tables

### User

- username (unique, primary key)
- email
- password
- redis (boolean)
- postgres (boolean)
- minio (boolean)
- milvus (boolean)
- mongodb (boolean)



## API

The API actions will be the following:

### listuser
GET all user records. 

### adduser
POST a new user (redis, postgres, minio, milvus, and mongo has to be inside an object named "options")

### deleteuser
DELETE the selected user by the username
