import os
from kubernetes import client, config


def get_config() -> client.Configuration:
    """Return a configured kubernetes client.Configuration.

    Prefers kubeconfig if present; otherwise builds from environment variables.
    """
    kubeconfig_path = os.environ.get("KUBECONFIG") or os.path.expanduser("~/.kube/config")
    if os.path.exists(kubeconfig_path):
        config.load_kube_config(config_file=kubeconfig_path)
        return client.Configuration.get_default_copy()

    api_server = os.environ.get("KUBE_HOST", "https://127.0.0.1:45089")
    api_token = os.environ.get("API_TOKEN") or os.environ.get("API_KEY")
    verify_ssl_env = os.environ.get("KUBE_VERIFY_SSL", "false").lower() in {"1", "true", "yes"}
    ca_cert_path = os.environ.get("KUBE_CA_FILE")

    configuration = client.Configuration()
    configuration.host = api_server
    configuration.verify_ssl = verify_ssl_env
    if ca_cert_path:
        configuration.ssl_ca_cert = ca_cert_path
    if api_token:
        configuration.api_key["authorization"] = api_token
        configuration.api_key_prefix["authorization"] = "Bearer"
    return configuration


def get_api_client() -> client.CoreV1Api:
    """Initialize CoreV1Api using the resolved configuration."""
    configuration = get_config()
    api_client = client.ApiClient(configuration)
    return client.CoreV1Api(api_client)