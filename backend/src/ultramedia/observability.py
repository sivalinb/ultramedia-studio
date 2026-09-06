import time
from contextlib import contextmanager
from uuid import uuid4

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from sqlalchemy import select

from .database import Database, TraceSpan


def configure_telemetry(endpoint: str | None, environment: str) -> None:
    if not endpoint or isinstance(trace.get_tracer_provider(), TracerProvider):
        return
    provider = TracerProvider(
        resource=Resource.create({"service.name": "ultramedia-api", "deployment.environment": environment})
    )
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=endpoint.startswith("http://")))
    )
    trace.set_tracer_provider(provider)


class TraceRecorder:
    """Privacy-minimized trace recorder; raw prompts and drafts are intentionally excluded."""

    def __init__(self, database: Database, trace_id: str | None = None):
        self.database = database
        self.trace_id = trace_id or str(uuid4())

    @contextmanager
    def stage(self, name: str, detail: str):
        started = time.perf_counter()
        status = "passed"
        tracer = trace.get_tracer("ultramedia.workflow")
        try:
            with tracer.start_as_current_span(name) as span:
                span.set_attribute("ultramedia.trace_id", self.trace_id)
                span.set_attribute("ultramedia.detail", detail)
                yield
        except Exception as error:
            status = "failed"
            span.record_exception(error)
            raise
        finally:
            elapsed = int((time.perf_counter() - started) * 1000)
            with self.database.session() as db:
                db.add(
                    TraceSpan(
                        trace_id=self.trace_id,
                        stage=name,
                        status=status,
                        duration_ms=max(1, elapsed),
                        detail=detail,
                    )
                )

    def spans(self) -> list[TraceSpan]:
        with self.database.session() as db:
            return list(
                db.scalars(select(TraceSpan).where(TraceSpan.trace_id == self.trace_id).order_by(TraceSpan.created_at))
            )
