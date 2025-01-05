from typing import AsyncIterator
from httpx_ws import aconnect_ws

from companion_client.model.chat import ChatStreamingRequest, ChatStreamingResponse


class CompanionChatClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def chat(self, request: ChatStreamingRequest) -> AsyncIterator[ChatStreamingResponse]:        
        async with aconnect_ws(f"{self.base_url}/chat/ws") as ws:
            await ws.send_text(request.model_dump_json())
            while True:
                message = await ws.receive_text()
                rsp = ChatStreamingResponse.model_validate_json(message)
                yield rsp

