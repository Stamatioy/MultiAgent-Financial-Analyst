from financial_analyst.api.jobs import (
    ResearchJobStore,
)
from financial_analyst.api.models import (
    ResearchJobStatus,
    ResearchStepStatus,
)


def test_create_job() -> None:
    store = ResearchJobStore()

    job_id = store.create(
        ticker="AMD"
    )

    result = store.status(
        job_id
    )

    assert result.ticker == "AMD"

    assert (
        result.status
        == ResearchJobStatus.QUEUED
    )

    assert result.progress == 0.0

    assert len(
        result.steps
    ) == 6


def test_update_job_progress() -> None:
    store = ResearchJobStore()

    job_id = store.create(
        ticker="AMD"
    )

    store.start(
        job_id
    )

    store.update_step(
        job_id=job_id,
        step_name="market",
        status=(
            ResearchStepStatus.RUNNING
        ),
    )

    running = store.status(
        job_id
    )

    assert (
        running.current_step
        == "market"
    )

    store.update_step(
        job_id=job_id,
        step_name="market",
        status=(
            ResearchStepStatus.COMPLETED
        ),
    )

    completed = store.status(
        job_id
    )

    assert completed.progress == (
        1 / 6
    )


def test_job_failure() -> None:
    store = ResearchJobStore()

    job_id = store.create(
        ticker="AMD"
    )

    store.start(
        job_id
    )

    store.update_step(
        job_id=job_id,
        step_name="valuation",
        status=(
            ResearchStepStatus.RUNNING
        ),
    )

    store.fail(
        job_id=job_id,
        error="Test failure",
    )

    result = store.status(
        job_id
    )

    assert (
        result.status
        == ResearchJobStatus.FAILED
    )

    assert result.error == (
        "Test failure"
    )

    valuation = next(
        step
        for step in result.steps
        if step.name
        == "valuation"
    )

    assert (
        valuation.status
        == ResearchStepStatus.FAILED
    )