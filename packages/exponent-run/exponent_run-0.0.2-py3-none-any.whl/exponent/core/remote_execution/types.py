from typing import ClassVar

from pydantic import BaseModel


class RemoteExecutionMessage(BaseModel):
    namespace: ClassVar[str] = "default"

    execution_uuid: str

    @property
    def result_key(self) -> str:
        return f"{self.namespace}:{self.execution_uuid}"


class RemoteExecutionRequest(RemoteExecutionMessage):
    pass


class RemoteExecutionResponse(RemoteExecutionMessage):
    pass


class CodeExecutionRequest(RemoteExecutionRequest):
    namespace: ClassVar[str] = "code_execution"

    code_block_uuid: str
    language: str
    content: str


class CodeExecutionResponse(RemoteExecutionResponse):
    namespace: ClassVar[str] = "code_execution"
    content: str


class CreateChatResponse(BaseModel):
    chat_uuid: str
