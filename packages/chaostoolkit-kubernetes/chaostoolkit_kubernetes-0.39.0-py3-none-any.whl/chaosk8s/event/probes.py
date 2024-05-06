import json
from typing import Any, Dict

from chaoslib.types import Configuration, Secrets
from kubernetes import client

from chaosk8s import create_k8s_api_client

__all__ = ["get_events"]


def get_events(
    label_selector: str = None,
    field_selector: str = None,
    limit: int = 100,
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Dict[str, Any]:
    """
    Retrieve Kubernetes events across all namespaces. If a `label_selector`
    is set, filter to that selector only.

    The right values for `field_selector` come from
    https://github.com/kubernetes/kubernetes/blob/d1a2a134c532109540025c990697a6900c2e62fc/pkg/apis/events/v1/conversion.go#L66
    """  # no: E501
    api = create_k8s_api_client(secrets)

    v1 = client.EventsV1Api(api)
    ret = v1.list_event_for_all_namespaces(
        _preload_content=False,
        label_selector=label_selector,
        field_selector=field_selector,
        limit=limit,
    )

    return json.loads(ret.read().decode("utf-8"))
