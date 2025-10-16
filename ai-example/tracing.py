import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from utils import read_secret

def setup_tracing(service_name):

    # Set environment variables for LangChain
    os.environ["LANGSMITH_OTEL_ENABLED"] = "true"
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_OTEL_ONLY"] = "true"

    token = read_secret("token")

    resource = Resource.create(
        {
            "gen_ai.agent.name": service_name,
            "service.name": service_name,
            "service.version": "0.0.1"
        }
    )

    # Configure the OTLP exporter for your custom endpoint
    provider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter(
        # Change to your provider's endpoint
        endpoint="https://xbw95514.dev.dynatracelabs.com/api/v2/otlp/v1/traces",
        # Add any required headers for authentication
        headers={"Authorization": f"Api-Token {token}"}
    )
    processor = SimpleSpanProcessor(otlp_exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Instrument MCP calls
    from opentelemetry.instrumentation.mcp import McpInstrumentor
    McpInstrumentor().instrument()