import sys, os, json
import kubernetes.client as client
from configure import get_config

def load_data(data: str) -> dict:
    """Load a Kubernetes Pod manifest from a file path (JSON) or inline JSON string."""
    if os.path.isfile(data):
        _, ext = os.path.splitext(data)
        with open(data, "r", encoding="utf-8") as f:
            data = f.read()
            data = json.loads(data)
    else:
        # Treat as inline JSON
        data = json.loads(data)
    return data

def create(config_file):
    configuration = get_config()
    crd_configuration = load_data(config_file)
    with client.ApiClient(configuration) as api_client:
        api = client.ApiextensionsV1Api(api_client)
        body = client.V1CustomResourceDefinition(
            metadata=client.V1ObjectMeta(name="examples.example.com"),
            spec=client.V1CustomResourceDefinitionSpec(
                group="example.com",
                scope="Namespaced",
                names=client.V1CustomResourceDefinitionNames(
                    plural="examples",
                    singular="example",
                    kind="Example",
                    short_names=["ex"],
                ),
                versions=[
                    client.V1CustomResourceDefinitionVersion(
                        name="v1",
                        served=True,
                        storage=True,
                        schema=client.V1CustomResourceValidation(
                            open_apiv3_schema=client.V1JSONSchemaProps(
                                type="object",
                                properties={
                                    "spec": client.V1JSONSchemaProps(type="object"),
                                    "status": client.V1JSONSchemaProps(type="object"),
                                },
                            )
                        ),
                    )
                ],
            ), 
        )
        try:
            return api.create_custom_resource_definition(body)
        except client.rest.ApiException as e:
            print("Exception when calling ApiextensionsV1Api->create_custom_resource_definition: %s\n" % e)

def delete(config_file):
    configuration = get_config()
    crd_configuration = load_data(config_file)
    with client.ApiClient(configuration) as api_client:
        api = client.ApiextensionsV1Api(api_client)
        body = client.V1CustomResourceDefinition(
            metadata=client.V1ObjectMeta(name="examples.example.com"),
            spec=client.V1CustomResourceDefinitionSpec(
                group="example.com",
                scope="Namespaced",
                names=client.V1CustomResourceDefinitionNames(
                    plural="examples",
                    singular="example",
                    kind="Example",
                    short_names=["ex"],
                ),
                versions=[
                    client.V1CustomResourceDefinitionVersion(
                        name="v1",
                        served=True,
                        storage=True,
                        schema=client.V1CustomResourceValidation(
                            open_apiv3_schema=client.V1JSONSchemaProps(
                                type="object",
                                properties={
                                    "spec": client.V1JSONSchemaProps(type="object"),
                                    "status": client.V1JSONSchemaProps(type="object"),
                                },
                            )
                        ),
                    )
                ],
            ), 
        )
        try:
            return api.create_custom_resource_definition(body)
        except client.rest.ApiException as e:
            print("Exception when calling ApiextensionsV1Api->create_custom_resource_definition: %s\n" % e)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: create_crd.py <config_file>")

    create(sys.argv[1])