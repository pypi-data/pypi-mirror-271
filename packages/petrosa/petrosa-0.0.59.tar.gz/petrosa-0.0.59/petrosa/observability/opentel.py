import os
from opentelemetry import metrics, trace

SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "no-service-name")

meter = metrics.get_meter(SERVICE_NAME)
tracer = trace.get_tracer(SERVICE_NAME)
