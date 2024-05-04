import asyncio
import logging
import os
import random
import traceback
from typing import Any, List, Union

import httpx

from creator.auto.request_auto import AutoTxt2Img, AutoModelLoad, AutoImg2Img
from creator.auto.response_auto import ResponseAuto
from creator.base.base_app import BaseApp
from creator.base.base_response import BaseResponse

logger = logging.getLogger(__name__)


class AppAuto(BaseApp):
    param_classes = [AutoTxt2Img, AutoImg2Img]
    output = {}
    jobs = {}

    def __init__(self):
        super().__init__()
        auto_port = os.environ.get("PORT_AUTO", 8081)
        if isinstance(auto_port, str):
            auto_port = int(auto_port)
        self.jobs = {}
        self.output = {}
        self.api_base_url = f"http://0.0.0.0:{auto_port}/sdapi"

    async def create(self, params: Union[AutoTxt2Img, AutoImg2Img], job_id=None) -> BaseResponse:
        print(f"Creating job with params: {params}")
        endpoint_name = "txt2img" if isinstance(params, AutoTxt2Img) else "img2img"
        url = f"{self.api_base_url}/sdapi/v1/{endpoint_name}"
        data = params.__dict__
        headers = {'Content-Type': 'application/json'}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, headers=headers)
            response.raise_for_status()
        output = response.json()
        print(f"Response received: {output}")
        if job_id:
            self.output[job_id] = output
        return ResponseAuto.parse_response(output)

    async def create_async(self, params: Union[AutoTxt2Img, AutoImg2Img]) -> BaseResponse:
        job_id = str(random.randint(0, 100000))
        print(f"Creating job with ID {job_id}")

        # Store the job_id immediately with a placeholder to indicate it's pending
        self.output[job_id] = {"status": "pending"}

        # Fire off the job without waiting for it to complete
        asyncio.create_task(self._create_job(params, job_id, self.output))

        # Return a response indicating that the job is running
        response = ResponseAuto.running(job_id)
        print(f"Job {job_id} is running.")
        return response

    async def get_status(self, job_id: str) -> BaseResponse:
        try:
            output = self.output.get(job_id)
            if output:
                # Check if the job resulted in an error
                if "error" in output:
                    print(f"Error found for job ID {job_id}")
                    return ResponseAuto.error(output["error"])
                print(f"Output found for job ID {job_id}")
                return ResponseAuto.parse_response(output)

            # If job_id is not in the jobs dictionary and no output is found, assume the job does not exist
            if job_id not in self.jobs:
                logger.warning(f"Job ID {job_id} not found")
                return ResponseAuto.error(f"Job ID {job_id} not found")

            # If the job is still in jobs but no output has been generated yet
            print(f"Job {job_id} is still running.")
            return ResponseAuto.running(job_id)

        except Exception as e:
            logger.error(f"Error getting job status for job ID {job_id}: {e}")
            traceback.print_exc()
            return ResponseAuto.error(f"Error getting job status: {e}")

    async def get_models(self) -> List[Any]:
        url = f"{self.api_base_url}/sdapi/v1/sd-models"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            response_json = response.json()
        models = [model.get("title") for model in response_json if model.get("title")]
        return models

    # Assuming you will provide more detail or use this method later
    async def upload_image(self, image_data: Any) -> str:
        pass

    async def select_model(self, params: AutoModelLoad):
        model_to_load = params.sd_model_checkpoint
        if model_to_load and model_to_load not in self.loaded_models:
            self.loaded_models.append(model_to_load)
        max_cached_models = os.environ.get("MAX_CACHED_MODELS", 3)
        if len(self.loaded_models) > max_cached_models:
            self.loaded_models = self.loaded_models[-max_cached_models:]
        url = f"{self.api_base_url}/sdapi/v1/options"
        headers = {'Content-Type': 'application/json'}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=params.__dict__, headers=headers)
            response.raise_for_status()
            return response.json()

    async def test(self):
        auto_port = int(os.environ.get("PORT_AUTO", 8081))
        url = f"http://0.0.0.0:{auto_port}/docs"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return BaseResponse.active()
            else:
                return BaseResponse.error("Error testing connection")

    async def _create_job(self, params: AutoTxt2Img, job_id: str, output_store: dict):
        url = f"{self.api_base_url}/v1/txt2img"  # Adjust URL as necessary
        data = params.__dict__
        headers = {'Content-Type': 'application/json'}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data, headers=headers)
                response.raise_for_status()
            output = response.json()
            print(f"Response received: {output}")
            output_store[job_id] = output  # Storing output for future retrieval
        except Exception as e:
            print(f"Error in job {job_id}: {e}")
            output_store[job_id] = {"error": str(e)}
