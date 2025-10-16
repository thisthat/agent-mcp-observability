import os
from traceloop.sdk import Traceloop
from utils import read_secret

def setup_tracing(service_name):
    os.environ['TRACELOOP_TELEMETRY'] = "false"
    os.environ["OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE"] = "delta"
    token = read_secret("token")
    headers = { "Authorization": f"Api-Token {token}" }
    resource = {
        "gen_ai.agent.name": service_name,
        "service.name": service_name,
        "service.version": "0.0.1"
    }
    Traceloop.init(
        app_name=service_name,
        api_endpoint="https://xbw95514.dev.dynatracelabs.com/api/v2/otlp",
        headers=headers,
        resource_attributes=resource,
    )