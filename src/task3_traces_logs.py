import logging
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

resource = Resource.create({"service.name": "a8-demo", "service.version": "1.0"})
ENDPOINT = "http://localhost:4317"

# Traces
tp = TracerProvider(resource=resource)
tp.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=ENDPOINT, insecure=True)))
trace.set_tracer_provider(tp)

# Logs：把 Python 內建的 logging 接到 OpenTelemetry
lp = LoggerProvider(resource=resource)
lp.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter(endpoint=ENDPOINT, insecure=True)))
set_logger_provider(lp)
logging.getLogger().addHandler(LoggingHandler(level=logging.INFO, logger_provider=lp))
logging.getLogger().setLevel(logging.INFO)
log = logging.getLogger("a8.demo")

tracer = trace.get_tracer("a8.demo")
with tracer.start_as_current_span("checkout"):
    log.info("start checkout")
    with tracer.start_as_current_span("charge-card"):
        log.warning("card charged", extra={"payment.amount": 299})

tp.shutdown()
lp.shutdown()
