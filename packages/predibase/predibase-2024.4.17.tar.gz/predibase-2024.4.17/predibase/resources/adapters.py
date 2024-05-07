from __future__ import annotations

import os
from typing import TYPE_CHECKING

from predibase._errors import FinetuningError
from predibase.config import FinetuningConfig
from predibase.resources.adapter import Adapter
from predibase.resources.dataset import Dataset
from predibase.resources.repo import Repo

# from predibase.resources.model import PretrainedHuggingFaceLLM, FinetunedLLMAdapter

if TYPE_CHECKING:
    from predibase import Predibase

_PATH_HERE = os.path.abspath(os.path.dirname(__file__))
_TEMPLATE_DIR = os.path.join(_PATH_HERE, "../resource/llm/templates")
_CONFIG_FILENAME = "config.yaml"  # Name of config file for loading templates.


class Adapters:
    def __init__(self, client: Predibase):
        self._client = client
        self._session = client._session  # Directly using the session in the short term as we transition to v2.

    def create(
        self,
        *,
        config: FinetuningConfig | dict,
        dataset: str | Dataset,
        repo: str | Repo,
        description: str | None = None,
        # show_tensorboard: bool = False,
    ) -> Adapter:

        # Always blocking since `watch` hardcoded to True.
        job = self._client.finetuning.jobs.create(
            config=config,
            dataset=dataset,
            repo=repo,
            description=description,
            watch=True,
            # show_tensorboard=show_tensorboard,
        )

        adapter_version_resp = self._client.http_get(f"/v2/repos/{job.target_repo}/version/{job.target_version_tag}")
        adapter = Adapter.model_validate(adapter_version_resp)

        if not adapter.artifact_path:
            raise FinetuningError(adapter.finetuning_error)

        return adapter

    def get(self, adapter_id: str) -> Adapter:
        adapter_version_resp = self._fetch(adapter_id)
        adapter = Adapter.model_validate(adapter_version_resp)

        if adapter_version_resp["status"] not in ("completed", "errored", "canceled"):
            # Training is still ongoing, so watch the progress and refetch after.
            print(f"Adapter {adapter_id} is not yet ready.")
            self._client.finetuning.jobs.watch(adapter.finetuning_job_uuid)

            adapter_version_resp = self._fetch(adapter_id)
            adapter = Adapter.model_validate(adapter_version_resp)

        if not adapter.artifact_path:
            raise FinetuningError(adapter.finetuning_error or "Unknown error - adapter not available.")

        return adapter

    def cancel(self, adapter_id: str):
        adapter_version_resp = self._fetch(adapter_id)
        adapter = Adapter.model_validate(adapter_version_resp)

        if not adapter.finetuning_job_uuid:
            raise RuntimeError(f"Adapter {adapter_id} is not associated with a cancelable finetuning job.")

        self._client.finetuning.jobs.cancel(adapter.finetuning_job_uuid)

    def download(self, adapter_id: str, dest: os.PathLike | None = None):
        repo, version_tag = self._parse_id(adapter_id)

        if dest is None:
            dest = os.path.join(os.getcwd(), f"{version_tag}.zip")

        print(f"Downloading adapter {adapter_id} to {dest}...")
        with self._client._http.get(
            self._client.api_gateway + f"/v2/repos/{repo}/version/{version_tag}/download",
            headers=self._client.default_headers,
        ) as r:
            with open(dest, "wb") as f:
                f.write(r.content)
        print("Done!")

    @staticmethod
    def _parse_id(adapter_id: str):
        segments = adapter_id.split("/", 1)
        if len(segments) != 2:
            raise ValueError("Expected adapter reference of the format <repo>/<version>.")

        return segments

    def _fetch(self, adapter_id: str):
        repo, version_tag = self._parse_id(adapter_id)
        adapter_version_endpoint = f"/v2/repos/{repo}/version/{version_tag}"

        return self._client.http_get(adapter_version_endpoint)
