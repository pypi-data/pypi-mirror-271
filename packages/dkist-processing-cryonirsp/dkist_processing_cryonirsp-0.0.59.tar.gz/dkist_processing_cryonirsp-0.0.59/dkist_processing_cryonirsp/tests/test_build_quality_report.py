import pytest
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.task_name import TaskName

from dkist_processing_cryonirsp.tasks.l1_output_data import CISubmitQuality
from dkist_processing_cryonirsp.tests.conftest import CryonirspConstantsDb


@pytest.fixture
def plot_data():
    datetimes_a = ["2021-01-01T01:01:01", "2021-01-01T02:01:01"]
    values_a = [3, 4]
    datetimes_b = ["2020-01-01T01:01:01", "2020-01-01T02:01:01"]
    values_b = [1, 2]
    return datetimes_a, values_a, datetimes_b, values_b


@pytest.fixture
def quality_task(tmp_path, recipe_run_id, init_cryonirsp_constants_db):
    constants_db = CryonirspConstantsDb(NUM_MODSTATES=2)
    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with CISubmitQuality(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(
            recipe_run_id=recipe_run_id,
            scratch_base_path=tmp_path,
        )
        task.scratch.workflow_base_path = tmp_path / str(recipe_run_id)
        yield task
        task._purge()


def test_build_report(quality_task, plot_data):
    """
    Given: a task with the QualityMixin and data on disk for multiple metrics
    When: building the quality report
    Then: the report is encoded with the expected schema
    """
    task = quality_task
    datetimes_a, values_a, _, _ = plot_data
    task.quality_store_task_type_counts(
        task_type=TaskName.dark.value, total_frames=100, frames_not_used=7
    )
    task.quality_store_fried_parameter(datetimes=datetimes_a, values=values_a)
    task.quality_store_light_level(datetimes=datetimes_a, values=values_a)
    task.quality_store_frame_average(
        datetimes=datetimes_a, values=values_a, task_type=TaskName.dark.value, modstate=1
    )
    task.quality_store_frame_average(
        datetimes=datetimes_a, values=values_a, task_type=TaskName.lamp_gain.value, modstate=1
    )
    task.quality_store_frame_rms(
        datetimes=datetimes_a, values=values_a, task_type=TaskName.dark.value, modstate=1
    )
    task.quality_store_frame_rms(
        datetimes=datetimes_a, values=values_a, task_type=TaskName.lamp_gain.value, modstate=1
    )
    task.quality_store_frame_average(
        datetimes=datetimes_a, values=values_a, task_type=TaskName.dark.value, modstate=2
    )
    task.quality_store_frame_average(
        datetimes=datetimes_a, values=values_a, task_type=TaskName.lamp_gain.value, modstate=2
    )
    task.quality_store_frame_rms(
        datetimes=datetimes_a, values=values_a, task_type=TaskName.dark.value, modstate=2
    )
    task.quality_store_frame_rms(
        datetimes=datetimes_a, values=values_a, task_type=TaskName.lamp_gain.value, modstate=2
    )
    task.quality_store_dataset_average(
        task_type=TaskName.dark.value, frame_averages=[1, 2, 3, 4, 5]
    )
    task.quality_store_dataset_average(
        task_type=TaskName.dark.value, frame_averages=[6, 7, 8, 9, 10]
    )
    task.quality_store_dataset_rms(task_type=TaskName.dark.value, frame_rms=[1, 2, 3, 4, 5])
    task.quality_store_dataset_rms(task_type=TaskName.dark.value, frame_rms=[6, 7, 8, 9, 10])
    task.quality_store_dataset_rms(task_type="gain", frame_rms=[6, 7, 8, 9, 10])
    task.quality_store_noise(datetimes=datetimes_a, values=values_a)
    task.quality_store_range(name="metric 1", warnings=["warning 1"])
    task.quality_store_range(name="metric 2", warnings=["warning 2"])
    task.quality_store_range(name="metric 3", warnings=["warning 3"])
    task.quality_store_health_status(values=["Good", "Good", "Good", "Good", "Good", "Ill"])
    task.quality_store_ao_status(values=[1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0])
    task.quality_store_sensitivity(datetimes=datetimes_a, values=values_a, stokes="I")
    task.quality_store_sensitivity(datetimes=datetimes_a, values=values_a, stokes="Q")
    task.quality_store_sensitivity(datetimes=datetimes_a, values=values_a, stokes="U")
    task.quality_store_sensitivity(datetimes=datetimes_a, values=values_a, stokes="V")
    task.quality_store_historical(name="hist 1", value=7)
    task.quality_store_historical(name="hist 2", value="abc")
    task.quality_store_historical(
        name="hist 3", value=9.35, warning="warning for historical metric 3"
    )

    report = task.quality_build_report()
    assert len(report) == 15
