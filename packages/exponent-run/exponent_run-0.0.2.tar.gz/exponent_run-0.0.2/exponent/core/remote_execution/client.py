import subprocess

from httpx import AsyncClient

from exponent.core.remote_execution.types import (
    CodeExecutionRequest,
    CodeExecutionResponse,
    CreateChatResponse,
)


class RemoteExecutionClient:
    def __init__(self, api_key: str, base_url: str, session: AsyncClient):
        self.headers = {"API-KEY": api_key}
        self.base_url = base_url
        self.session = session

    async def get_execution_requests(
        self, chat_uuid: str
    ) -> list[CodeExecutionRequest]:
        response = await self.session.get(
            f"{self.base_url}/api/remote_execution/{chat_uuid}/requests",
            headers=self.headers,
        )
        results = response.json()
        return [CodeExecutionRequest(**result) for result in results]

    async def post_execution_result(
        self, chat_uuid: str, code_execution_response: CodeExecutionResponse
    ) -> None:
        await self.session.post(
            f"{self.base_url}/api/remote_execution/{chat_uuid}/result",
            headers=self.headers,
            json=code_execution_response.model_dump(),
        )

    async def create_chat(self) -> CreateChatResponse:
        response = await self.session.post(
            f"{self.base_url}/api/remote_execution/create_chat",
            headers=self.headers,
        )
        return CreateChatResponse(**response.json())

    def execute_code(
        self, code_execution_request: CodeExecutionRequest
    ) -> CodeExecutionResponse:
        if code_execution_request.language == "python":
            return CodeExecutionResponse(
                content="hi im a python result",
                execution_uuid=code_execution_request.execution_uuid,
            )
        elif code_execution_request.language == "shell":
            try:
                shell_output = subprocess.check_output(
                    code_execution_request.content,
                    shell=True,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
            except subprocess.CalledProcessError as e:
                shell_output = e.output

            code_execution_result = CodeExecutionResponse(
                content=shell_output,
                execution_uuid=code_execution_request.execution_uuid,
            )
            return code_execution_result
        else:
            raise ValueError(f"Unsupported language: {code_execution_request.language}")
