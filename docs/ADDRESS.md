# ops admin
These API are used to interact with the k8s cluster, imitating the "ops admin" CLI command. Users are defined with the interface:
```
{
    "name": string, // min 5 characters, max length: 61 chars, only numbers or lower case characters
    "email: string, // email type
    "password": string,
    "options": {
      "redis": boolean,
      "mongo": boolean,
      "postgres": boolean,
      "minio": boolean,
      "seaweed": boolean,
      "milvus": boolean
    }
  }
```

## listuser()
revceives the list of all registered users.

### Request
GET /api/v1/web/devel/kube/listuser

### Response
Array of User objects:
[
  {
    "name": string,
    "email: string,
    "redis": boolean,
    "mongo": boolean,
    "postgres": boolean,
    "minio": boolean,
    "seaweed": boolean,
    "milvus": boolean
  },
]


## adduser()
revceives the list of all registered users.

### Request
POST /api/v1/web/devel/kube/adduser

{
  "name": string,
  "email": string,
  "password": string,
  "redis": boolean,
  "mongo": boolean,
  "postgres": boolean,
  "minio": boolean,
  "seaweed": boolean,
  "milvus": boolean
}


## deleteuser()
revceives the list of all registered users.

### Request
POST /api/v1/web/devel/kube/deleteuser

{
  "name": string,
}
