from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

provider = TracerProvider(resource=Resource.create({"service.name": "a8-demo"}))
# 只換 exporter：從 Console 改成 OTLP，送到 collector
exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("a8.demo")
with tracer.start_as_current_span("checkout") as parent:
    parent.set_attribute("order.id", "A001")
    with tracer.start_as_current_span("charge-card") as child:
        child.set_attribute("payment.amount", 299)
        print("paid")

# Batch 會先暫存，程式結束前一定要 flush，否則資料可能還沒送出去
provider.shutdown()
