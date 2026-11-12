from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# 1) TracerProvider：追蹤功能的「總管」，resource 標示這是哪個服務
provider = TracerProvider(resource=Resource.create({"service.name": "a8-demo"}))
# 2) Processor + Exporter：span 一結束就交給 ConsoleSpanExporter 印到終端機
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("a8.demo")

# 3) 父 span 包住子 span，形成階層
with tracer.start_as_current_span("checkout") as parent:
    parent.set_attribute("order.id", "A001")
    with tracer.start_as_current_span("charge-card") as child:
        child.set_attribute("payment.amount", 299)
        print("paid")
