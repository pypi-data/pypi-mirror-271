import asyncio
import base64
import dataclasses
import json
import logging
import os
import urllib
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

import httpx
import requests

from creator.base.base_app import BaseApp
from creator.base.base_request import BaseRequest
from creator.base.base_response import ResponseDataType, ResponseData, BaseResponse
from creator.base.job_status import JobStatus
from creator.cmfy.request_cmfy import CmfyWorkflow
from creator.cmfy.response_cmfy import ResponseCmfy

logger = logging.getLogger(__name__)


class AppCmfy(BaseApp):
    param_classes = [CmfyWorkflow]
    output = {}

    def __init__(self):
        super().__init__()
        focus_port = os.environ.get("PORT_CMFY", 8888)
        if isinstance(focus_port, str):
            focus_port = int(focus_port)
        self.api_base_url = f"http://0.0.0.0:{focus_port}"

    async def create(self, params: CmfyWorkflow) -> ResponseCmfy:
        cmfy_port = os.environ.get("PORT_CMFY", 8889)
        url = f"http://localhost:{cmfy_port}/prompt"
        workflow = json.loads(params.workflow_json)
        self._check_loaded_model(workflow)
        logger.debug(f"CMFY data: {workflow}")
        # Send a POST to cmfy_url with the workflow json
        # The response will be JSON string with the below format
        try:
            headers = {'Content-Type': 'application/json'}
            data = {"prompt": workflow}
            data = json.dumps(data).encode('utf-8')
            response = requests.post(url, data=data, headers=headers)
            logger.debug(f"CMFY response: {response}, {response.text}, {response.json()}")
            # If we have a 422 here, print what the unprocessable entity is
            if response.status_code == 422:
                logger.warning(f"Unprocessable entity: {response.text}")
            response.raise_for_status()
            response_json = response.json()
        except Exception as e:
            logger.error(f"Error creating prompt: {e}")
            return ResponseCmfy.error("Error creating prompt")
        # {"prompt_id": "f57c69ee-f4ed-4866-b5a4-4072c17c36a8", "number": 2, "node_errors": {}}
        prompt_id = response_json.get("prompt_id", None)
        logger.debug(f"Prompt ID: {prompt_id}")
        if prompt_id is None:
            return ResponseCmfy.error("Error creating prompt")
        status_count = 0
        status = await self.get_status(prompt_id)
        while status != JobStatus.FINISHED and status != JobStatus.FAILED and status_count < 10:
            await asyncio.sleep(1)
            status = await self.get_status(prompt_id)
            status_count += 1
        if status == JobStatus.FINISHED:
            data = self.output
            response_data = ResponseData(
                data=data,
                data_type=ResponseDataType.IMAGE,
                total_count=len(data)
            )
            logger.info(f"Success, returning response with {len(data)} images")
            return ResponseCmfy.success(response_data)
        return ResponseCmfy.error("Error creating prompt")

    async def create_async(self, params: CmfyWorkflow) -> ResponseCmfy:
        cmfy_port = os.environ.get("PORT_CMFY", 8889)
        url = f"http://localhost:{cmfy_port}/prompt"
        workflow = json.loads(params.workflow_json)
        self._check_loaded_model(workflow)
        logger.debug(f"CMFY data: {workflow}")
        # Send a POST to cmfy_url with the workflow json
        # The response will be JSON string with the below format
        try:
            headers = {'Content-Type': 'application/json'}
            data = {"prompt": workflow}
            data = json.dumps(data).encode('utf-8')
            response = requests.post(url, data=data, headers=headers)
            logger.debug(f"CMFY response: {response}, {response.text}, {response.json()}")
            # If we have a 422 here, print what the unprocessable entity is
            if response.status_code == 422:
                logger.warning(f"Unprocessable entity: {response.text}")
            response.raise_for_status()
            response_json = response.json()
        except Exception as e:
            logger.error(f"Error creating prompt: {e}")
            return ResponseCmfy.error("Error creating prompt")
        # {"prompt_id": "f57c69ee-f4ed-4866-b5a4-4072c17c36a8", "number": 2, "node_errors": {}}
        prompt_id = response_json.get("prompt_id", None)
        logger.debug(f"Prompt ID: {prompt_id}")
        if prompt_id is None:
            return ResponseCmfy.error("Error creating prompt")
        return ResponseCmfy.running(prompt_id)

    async def get_status(self, job_id) -> BaseResponse:
        url = f"http://localhost:{os.environ.get('PORT_CMFY', 8889)}/history/{job_id}"
        job_data = None
        print(f"Getting status for job {job_id} from url {url}")
        logger.debug(f"Getting status for job {job_id}")
        while job_data is None:
            history = requests.get(url)
            if history.status_code != 200:
                return BaseResponse.error("Error getting job status")
            logger.info(f"History: {history.json()}")
            history = history.json()
            for history_id, job in history.items():
                if history_id == job_id:
                    job_data = job
                    break
        images_output = []
        for node_id, node_output in job_data['outputs'].items():
            if 'images' in node_output:
                logger.debug(f"Node output: {node_output}")
                for image in node_output['images']:
                    logger.debug(f"Getting image: {image['filename']}")
                    print(f"Getting image: {image['filename']}")
                    image_data = await self._get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                print(f"We are returning {len(images_output)} images")
                response_data = ResponseData(data=images_output, data_type=ResponseDataType.IMAGE,
                                             total_count=len(images_output))
                return ResponseCmfy.success(response_data)
        response = ResponseCmfy.running(job_id)
        return response

    async def get_models(self) -> List[Any]:
        url = f"http://localhost:{os.environ.get('PORT_CMFY', 8889)}/object_info"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            response_json = response.json()
            models = []
            loader = response_json.get("CheckpointLoaderSimple", None)
            if loader:
                input = loader.get("input", None)
                if input:
                    required = input.get("required", None)
                    if required:
                        model_name = required.get("ckpt_name", None)
                        if model_name:
                            models.append(model_name)
        return models

    async def upload_image(self, image_data: Any) -> str:
        pass

    async def select_model(self, params: BaseRequest):
        pass

    async def test(self):
        url = f"http://localhost:{os.environ.get('PORT_CMFY', 8889)}/history"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return BaseResponse.active()
            else:
                return BaseResponse.error("Error testing connection")

    @staticmethod
    async def _get_image(filename: str, subfolder: str, folder_type: str) -> Optional[str]:
        server_address = f"localhost:{os.environ.get('PORT_CMFY', 8889)}"
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        req_url = f"http://{server_address}/view?{url_values}"
        logger.debug(f"Getting image from {req_url}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(req_url)
                response.raise_for_status()
                image_data = response.content
                # Convert the image data to a base64 string
                base64_encoded = base64.b64encode(image_data).decode('utf-8')
                print(f"Image data: {base64_encoded[:100]}")
                return base64_encoded
        except Exception as e:
            logger.error(f"Failed to retrieve or encode image: {e}")
            return None

    def _check_loaded_model(self, workflow: Dict[str, Any]):
        for node_id, node in workflow.items():
            try:
                if node['class_type'] == "CheckpointLoaderSimple":
                    model_name = node['inputs']['ckpt_name']
                    if model_name and model_name not in self.loaded_models:
                        self.loaded_models.append(model_name)
            except KeyError:
                continue
        max_cached_models = os.environ.get("MAX_CACHED_MODELS", 3)
        if len(self.loaded_models) > max_cached_models:
            self.loaded_models = self.loaded_models[-max_cached_models:]
