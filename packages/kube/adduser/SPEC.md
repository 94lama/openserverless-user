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


## Adduser method

The creation of the user, consists in the creation of a Kubernetes CRD, which follows the structure:

```user-crd.yaml
apiVersion: nuvolaris.org/v1
kind: WhiskUser
metadata:
  name: ${USERNAME}
  namespace: nuvolaris
spec:
  email: ${EMAIL}
  password: ${PASSWORD}
  namespace: ${USERNAME}
  auth: ${SECRET_USER_AUTH}
  redis:
    enabled: ${REDIS_ENABLED}
    prefix: ${USERNAME}
    password: ${USER_SECRET_REDIS}
  mongodb:
    enabled: ${MONGODB_ENABLED}
    database: ${USERNAME}
    password: ${USER_SECRET_MONGODB}
  postgres:
    enabled: ${POSTGRES_ENABLED}
    database: ${USERNAME}
    password: ${USER_SECRET_POSTGRES}
  object-storage:
    password: ${USER_SECRET_MINIO}
    quota: "${MINIO_STORAGE_QUOTA:-auto}"
    data:
      enabled: ${MINIO_DATA_ENABLED}
      bucket: ${USERNAME}-data
    route:
      enabled: ${MINIO_STATIC_ENABLED}
      bucket: ${USERNAME}-web
  milvus:
    enabled: ${MILVUS_ENABLED}
    database: ${USERNAME}
    password: ${USER_SECRET_MILVUS}
```