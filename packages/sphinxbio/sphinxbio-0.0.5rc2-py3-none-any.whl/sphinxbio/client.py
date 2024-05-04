import base64
import time
from typing import Optional

import cloudpickle
from pydantic import BaseModel

from sphinxbio.dataset_schemas.types.dataset_schema import DatasetSchema
from sphinxbio.dataset_schemas.types.register_dataset_schema import (
    RegisterDatasetSchema,
)
from sphinxbio.datasets.types.create_dataset import CreateDataset

from .base_client import (
    AsyncBaseSphinxBio,
    BaseSphinxBio,
    # Reexport from base_client
    SphinxbioEnvironment,  # noqa: F401
)


class SphinxBio(BaseSphinxBio):
    __doc__ = BaseSphinxBio.__doc__

    def register_dataset_schema(
        self, *, pydantic_model: BaseModel, campaign_id: Optional[str] = None
    ) -> DatasetSchema:
        raw_pickle = cloudpickle.dumps(pydantic_model)
        stringified_pickle = base64.b64encode(raw_pickle).decode()

        if campaign_id is None:
            campaign_id = self.campaigns.list_campaigns().data[0].id

        model_name = pydantic_model.__name__  # type: ignore
        return self.dataset_schemas.register_dataset_schema(
            request=RegisterDatasetSchema(
                className=model_name,
                cloudPickle=stringified_pickle,
                campaignId=campaign_id,
            ),
        )

    def create_dataset_from_file(self, *, filename: str, campaign_id: str):
        res = self.storage.get_presigned_url_for_upload(filename=filename)
        with open(filename, "rb") as f:
            files = {"file": (filename.split("/")[-1], f)}
            self._client_wrapper.httpx_client.request(
                url=res.presigned_response.url,
                method="POST",
                data=res.presigned_response.fields,
                files=files,
            )

        task_id = self.datasets.create_dataset(
            request=CreateDataset(
                name=filename,
                campaignId=campaign_id,
                stagedUploadPath=res.path,
            )
        ).task_id

        while True:
            task = self.external_tasks.get_task(task_id=task_id)
            if task.status == "SUCCESS":
                assert task.result.type == "CREATE_DATASET"
                return task.result.dataset_id
            elif task.status == "FAILED":
                raise Exception(f"Task failed: {task.error}")
            else:
                time.sleep(3)


class AsyncSphinxBio(AsyncBaseSphinxBio):
    __doc__ = AsyncBaseSphinxBio.__doc__

    pass
