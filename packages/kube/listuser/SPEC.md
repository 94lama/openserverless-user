# Description
This action allows to interact with OpenServerless' Kubernetes cluster, to get the list of all users.
The task is to:
- receive the request, query k8s, and return the list of objects
- write both unit and integration tests in a "test" sub-directory

# If invoked with the method GET
It will look for all Kubernetes Objects defined by the CRD "whisksusers.nuvolaris.org", and return them as a list with the following properties:
- name: string, [a-z, 0-9]{5,61}
- email: string
- redis: boolean,
- mongo: boolean,
- postgres: boolean,
- minio: boolean,
- seaweedFS: boolean,
- milvus: boolean