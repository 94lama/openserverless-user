# Description
This action allows to interact with OpenServerless' Kubernetes cluster, to delete an existing user, with all the related services.

# If invoked with the method POST
It will look for all Kubernetes Objects defined by the CRD "whisksusers.nuvolaris.org", find the opbecjt wih the "name" parameter which matches with args["name"], and DELETEss it.

## REQUEST
{
  "name": string
}