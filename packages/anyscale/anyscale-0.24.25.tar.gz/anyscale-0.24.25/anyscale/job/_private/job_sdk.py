from typing import Any, Dict, Optional
import uuid

from anyscale._private.models.image_uri import ImageURI
from anyscale._private.workload import WorkloadSDK
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import (
    CreateInternalProductionJob,
    InternalProductionJob,
    ProductionJobConfig,
)
from anyscale.client.openapi_client.models.production_job import ProductionJob
from anyscale.client.openapi_client.models.ray_runtime_env_config import (
    RayRuntimeEnvConfig,
)
from anyscale.job.models import JobConfig, JobState, JobStatus
from anyscale.sdk.anyscale_client.models.ha_job_states import HaJobStates
from anyscale.utils.runtime_env import parse_requirements_file


logger = BlockLogger()


class JobSDK(WorkloadSDK):
    def _populate_runtime_env(
        self,
        config: JobConfig,
        *,
        autopopulate_in_workspace: bool = True,
        cloud_id: Optional[str] = None,
        workspace_requirements_path: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Populates a runtime_env from the config.

        Local directories specified in the 'working_dir' will be uploaded and
        replaced with the resulting remote URIs.

        Requirements files will be loaded and populated into the 'pip' field.

        If autopopulate_from_workspace is passed and this code is running inside a
        workspace, the following defaults will be applied:
            - 'working_dir' will be set to '.'.
            - 'pip' will be set to the workspace-managed requirements file.
        """
        runtime_env: Dict[str, Any] = {}
        [runtime_env] = self.override_and_upload_local_dirs(
            [runtime_env],
            working_dir_override=config.working_dir,
            excludes_override=config.excludes,
            cloud_id=cloud_id,
            autopopulate_in_workspace=autopopulate_in_workspace,
            additional_py_modules=config.py_modules,
        )
        [runtime_env] = self.override_and_load_requirements_files(
            [runtime_env],
            requirements_override=config.requirements,
            workspace_requirements_path=workspace_requirements_path,
        )
        [runtime_env] = self.update_env_vars(
            [runtime_env], env_vars_updates=config.env_vars,
        )

        return runtime_env or None

    def _get_default_name(self) -> str:
        """Get a default name for the job.

        If running inside a workspace, this is generated from the workspace name,
        else it generates a random name.
        """
        # TODO(edoakes): generate two random words instead of UUID here.
        name = f"job-{self.get_current_workspace_name() or str(uuid.uuid4())}"
        self.logger.info(f"No name was specified, using default: '{name}'.")
        return name

    def submit(self, config: JobConfig) -> str:
        name = config.name or self._get_default_name()

        build_id = None
        if config.containerfile is not None:
            build_id = self.client.get_cluster_env_build_id_from_containerfile(
                cluster_env_name=f"image-for-job-{name}",
                containerfile=self.get_containerfile_contents(config.containerfile),
            )
        elif config.image_uri is not None:
            build_id = self.client.get_cluster_env_build_id_from_image_uri(
                image_uri=ImageURI.from_str(config.image_uri)
            )

        if self.enable_image_build_for_tracked_requirements:
            requirements_path_to_be_populated_in_runtime_env = None
            requirements_path = self.client.get_workspace_requirements_path()
            if requirements_path is not None:
                requirements = parse_requirements_file(requirements_path)
                if requirements:
                    build_id = self.client.build_image_from_requirements(
                        cluster_env_name=f"image-for-job-{name}",
                        base_build_id=self.client.get_default_build_id(),
                        requirements=requirements,
                    )
        else:
            requirements_path_to_be_populated_in_runtime_env = (
                self.client.get_workspace_requirements_path()
            )

        if build_id is None:
            build_id = self.client.get_default_build_id()

        compute_config_id, cloud_id = self.resolve_compute_config(config.compute_config)

        env_vars_from_workspace = self.client.get_workspace_env_vars()
        if env_vars_from_workspace:
            if config.env_vars:
                # the precedence should be cli > workspace
                env_vars_from_workspace.update(config.env_vars)
                config = config.options(env_vars=env_vars_from_workspace)
            else:
                config = config.options(env_vars=env_vars_from_workspace)

        runtime_env = self._populate_runtime_env(
            config,
            cloud_id=cloud_id,
            workspace_requirements_path=requirements_path_to_be_populated_in_runtime_env,
        )

        job: InternalProductionJob = self.client.submit_job(
            CreateInternalProductionJob(
                name=name,
                project_id=self.client.get_project_id(parent_cloud_id=cloud_id),
                workspace_id=self.client.get_current_workspace_id(),
                config=ProductionJobConfig(
                    entrypoint=config.entrypoint,
                    runtime_env=runtime_env,
                    build_id=build_id,
                    compute_config_id=compute_config_id,
                    max_retries=config.max_retries,
                ),
                # TODO(edoakes): support job queue config.
                job_queue_config=None,
            )
        )

        self.logger.info(f"Job '{name}' submitted, ID: '{job.id}'.")
        self.logger.info(
            f"View the job in the UI: {self.client.get_job_ui_url(job.id)}"
        )
        return job.id

    _HA_JOB_STATE_TO_JOB_STATE = {
        HaJobStates.UPDATING: JobState.RUNNING,
        HaJobStates.RUNNING: JobState.RUNNING,
        HaJobStates.RESTARTING: JobState.RUNNING,
        HaJobStates.CLEANING_UP: JobState.RUNNING,
        HaJobStates.PENDING: JobState.STARTING,
        HaJobStates.AWAITING_CLUSTER_START: JobState.STARTING,
        HaJobStates.SUCCESS: JobState.SUCCEEDED,
        HaJobStates.ERRORED: JobState.FAILED,
        HaJobStates.TERMINATED: JobState.FAILED,
        HaJobStates.BROKEN: JobState.FAILED,
        HaJobStates.OUT_OF_RETRIES: JobState.FAILED,
    }

    def _job_model_to_status(self, model: ProductionJob) -> JobStatus:
        ha_state = model.state.current_state if model.state else None
        state = self._HA_JOB_STATE_TO_JOB_STATE.get(ha_state, JobState.UNKNOWN)

        prod_job_config: ProductionJobConfig = model.config
        runtime_env_config: RayRuntimeEnvConfig = prod_job_config.runtime_env if prod_job_config else None
        config = JobConfig(
            name=model.name,
            compute_config=self.get_user_facing_compute_config(
                prod_job_config.compute_config_id
            ),
            requirements=runtime_env_config.pip if runtime_env_config else None,
            working_dir=runtime_env_config.working_dir if runtime_env_config else None,
            env_vars=runtime_env_config.env_vars if runtime_env_config else None,
            entrypoint=prod_job_config.entrypoint,
            max_retries=prod_job_config.max_retries
            if prod_job_config.max_retries is not None
            else -1,
        )

        return JobStatus(name=model.name, id=model.id, state=state, config=config)

    def _resolve_to_job_model(
        self, name: Optional[str] = None, job_id: Optional[str] = None
    ) -> ProductionJob:
        if name is None and job_id is None:
            raise ValueError("One of 'name' or 'job_id' must be provided.")

        if name is not None and job_id is not None:
            raise ValueError("Only one of 'name' or 'job_id' can be provided.")

        model: Optional[ProductionJob] = self.client.get_job(name=name, job_id=job_id)
        if model is None:
            if name is not None:
                raise RuntimeError(f"Job with name '{name}' was not found.")
            else:
                raise RuntimeError(f"Job with id '{job_id}' was not found.")

        return model

    def status(
        self, name: Optional[str] = None, job_id: Optional[str] = None
    ) -> JobStatus:
        job_model = self._resolve_to_job_model(name=name, job_id=job_id)
        return self._job_model_to_status(job_model)

    def terminate(
        self, job_id: Optional[str] = None, name: Optional[str] = None,
    ) -> str:
        job_model = self._resolve_to_job_model(name=name, job_id=job_id)
        self.client.terminate_job(job_model.id)
        self.logger.info(f"Marked job '{job_model.name}' for termination")
        return job_model.id

    _TERMINAL_JOB_STATES = [
        HaJobStates.SUCCESS,
        HaJobStates.TERMINATED,
        HaJobStates.OUT_OF_RETRIES,
    ]

    def archive(self, job_id: Optional[str] = None, name: Optional[str] = None,) -> str:
        job_model = self._resolve_to_job_model(name=name, job_id=job_id)

        ha_state = job_model.state.current_state if job_model.state else None
        if ha_state not in self._TERMINAL_JOB_STATES:
            raise RuntimeError(
                f"Job with id '{job_model.id}' has not reached a terminal state and cannot be archived."
            )

        self.client.archive_job(job_model.id)
        self.logger.info(f"Job {job_model.id} is successfully archived.")
        return job_model.id
