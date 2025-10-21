# Description
This action allows to interact with OpenServerless' Kubernetes cluster, to add a new user, with all selected services:
- Redis
- Mongo
- Minio
- SeaweedFS (in alternative to Minio)
- Milvus

# If invoked with the method POST
It will look for all Kubernetes Objects defined by the CRD "whisksusers.nuvolaris.org", and add a new user Object

## Request
The body of the request will have a JSON object with the interface:
{
  "name": string,
  "email": string,
  "redis": boolean,
  "mongo": boolean,
  "postgres": boolean,
  "minio": boolean,
  "seaweed": boolean,
  "milvus": boolean
}