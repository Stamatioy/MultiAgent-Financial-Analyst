from __future__ import annotations

from threading import Lock
from uuid import uuid4

from financial_analyst.api.models import (
    ResearchJobStatus,
    ResearchJobStatusResponse,
    ResearchStep,
    ResearchStepStatus,
)
from financial_analyst.committee.models import (
    CompanyInvestmentReport,
)


STEP_DEFINITIONS = [
    (
        "market",
        "Market Analysis",
    ),
    (
        "fundamentals",
        "Fundamental Analysis",
    ),
    (
        "valuation",
        "Valuation Analysis",
    ),
    (
        "risk",
        "Risk Analysis",
    ),
    (
        "news",
        "News Intelligence",
    ),
    (
        "committee",
        "Investment Committee",
    ),
]


class ResearchJobRecord:
    def __init__(
        self,
        *,
        job_id: str,
        ticker: str,
    ) -> None:
        self.job_id = job_id
        self.ticker = ticker

        self.status = (
            ResearchJobStatus.QUEUED
        )

        self.current_step: str | None = None

        self.steps = [
            ResearchStep(
                name=name,
                label=label,
            )
            for name, label
            in STEP_DEFINITIONS
        ]

        self.error: str | None = None

        self.report: (
            CompanyInvestmentReport
            | None
        ) = None


class ResearchJobStore:
    def __init__(self) -> None:
        self._jobs: dict[
            str,
            ResearchJobRecord,
        ] = {}

        self._lock = Lock()

    def create(
        self,
        *,
        ticker: str,
    ) -> str:
        job_id = str(
            uuid4()
        )

        record = ResearchJobRecord(
            job_id=job_id,
            ticker=ticker,
        )

        with self._lock:
            self._jobs[
                job_id
            ] = record

        return job_id

    def _get_record(
        self,
        job_id: str,
    ) -> ResearchJobRecord:
        record = self._jobs.get(
            job_id
        )

        if record is None:
            raise KeyError(
                job_id
            )

        return record

    def start(
        self,
        job_id: str,
    ) -> None:
        with self._lock:
            record = self._get_record(
                job_id
            )

            record.status = (
                ResearchJobStatus.RUNNING
            )

    def update_step(
        self,
        *,
        job_id: str,
        step_name: str,
        status: ResearchStepStatus,
    ) -> None:
        with self._lock:
            record = self._get_record(
                job_id
            )

            step = next(
                (
                    item
                    for item
                    in record.steps
                    if item.name
                    == step_name
                ),
                None,
            )

            if step is None:
                raise ValueError(
                    "Unknown research step: "
                    f"{step_name}"
                )

            step.status = status

            if (
                status
                == ResearchStepStatus.RUNNING
            ):
                record.current_step = (
                    step_name
                )

            elif (
                status
                == ResearchStepStatus.COMPLETED
                and record.current_step
                == step_name
            ):
                record.current_step = None

    def complete(
        self,
        *,
        job_id: str,
        report: CompanyInvestmentReport,
    ) -> None:
        with self._lock:
            record = self._get_record(
                job_id
            )

            record.report = report

            record.status = (
                ResearchJobStatus.COMPLETED
            )

            record.current_step = None

    def fail(
        self,
        *,
        job_id: str,
        error: str,
    ) -> None:
        with self._lock:
            record = self._get_record(
                job_id
            )

            record.status = (
                ResearchJobStatus.FAILED
            )

            record.error = error

            if (
                record.current_step
                is not None
            ):
                for step in record.steps:
                    if (
                        step.name
                        == record.current_step
                    ):
                        step.status = (
                            ResearchStepStatus.FAILED
                        )

            record.current_step = None

    def status(
        self,
        job_id: str,
    ) -> ResearchJobStatusResponse:
        with self._lock:
            record = self._get_record(
                job_id
            )

            completed = sum(
                1
                for step
                in record.steps
                if step.status
                == ResearchStepStatus.COMPLETED
            )

            total = len(
                record.steps
            )

            progress = (
                completed / total
                if total
                else 0.0
            )

            if (
                record.status
                == ResearchJobStatus.COMPLETED
            ):
                progress = 1.0

            return ResearchJobStatusResponse(
                job_id=record.job_id,

                ticker=record.ticker,

                status=record.status,

                current_step=(
                    record.current_step
                ),

                progress=progress,

                steps=[
                    step.model_copy(
                        deep=True
                    )
                    for step
                    in record.steps
                ],

                error=record.error,
            )

    def result(
        self,
        job_id: str,
    ) -> CompanyInvestmentReport:
        with self._lock:
            record = self._get_record(
                job_id
            )

            if record.report is None:
                raise ValueError(
                    "Research report is not ready."
                )

            return record.report


research_job_store = (
    ResearchJobStore()
)