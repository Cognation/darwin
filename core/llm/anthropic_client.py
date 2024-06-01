import datetime
import zoneinfo
from typing import Optional

from anthropic import AsyncAnthropic, RateLimitError
from httpx import Timeout

from core.config import LLMProvider
from core.llm.convo import Convo
from core.log import get_logger

from .base import BaseLLMClient

log = get_logger(__name__)

# Maximum number of tokens supported by Anthropic Claude 3
MAX_TOKENS = 4096


class AnthropicClient(BaseLLMClient):
    provider = LLMProvider.ANTHROPIC

    def _init_client(self):
        self.client = AsyncAnthropic(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            timeout=Timeout(
                max(self.config.connect_timeout, self.config.read_timeout),
                connect=self.config.connect_timeout,
                read=self.config.read_timeout,
            ),
        )
        self.stream_handler = self.stream_handler

    def _adapt_messages(self, convo: Convo) -> list[dict[str, str]]:
        """
        Adapt the conversation messages to the format expected by the Anthropic Claude model.

        Claude only recognizes "user" and "assistant" roles, and requires them to be switched
        for each message (ie. no consecutive messages from the same role).

        :param convo: Conversation to adapt.
        :return: Adapted conversation messages.
        """
        messages = []
        for msg in convo.messages:
            if msg["role"] == "function":
                raise ValueError("Anthropic Claude doesn't support function calling")

            role = "user" if msg["role"] in ["user", "system"] else "assistant"
            if messages and messages[-1]["role"] == role:
                messages[-1]["content"] += "\n\n" + msg["content"]
            else:
                messages.append(
                    {
                        "role": role,
                        "content": msg["content"],
                    }
                )
        return messages

    async def _make_request(
        self,
        convo: Convo,
        temperature: Optional[float] = None,
        json_mode: bool = False,
    ) -> tuple[str, int, int]:
        messages = self._adapt_messages(convo)
        completion_kwargs = {
            "max_tokens": MAX_TOKENS,
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature if temperature is None else temperature,
        }
        if json_mode:
            completion_kwargs["response_format"] = {"type": "json_object"}

        response = []
        async with self.client.messages.stream(**completion_kwargs) as stream:
            async for content in stream.text_stream:
                response.append(content)
                if self.stream_handler:
                    await self.stream_handler(content)

            # TODO: get tokens from the final message
            final_message = await stream.get_final_message()
            final_message.content

        response_str = "".join(response)

        # Tell the stream handler we're done
        if self.stream_handler:
            await self.stream_handler(None)

        return response_str, final_message.usage.input_tokens, final_message.usage.output_tokens

    def rate_limit_sleep(self, err: RateLimitError) -> Optional[datetime.timedelta]:
        """
        Anthropic rate limits docs:
        https://docs.anthropic.com/en/api/rate-limits#response-headers
        Limit reset times are in RFC 3339 format.

        """
        headers = err.response.headers
        if "anthropic-ratelimit-tokens-remaining" not in headers:
            return None

        remaining_tokens = headers["anthropic-ratelimit-tokens-remaining"]
        if remaining_tokens == 0:
            relevant_dt = headers["anthropic-ratelimit-tokens-reset"]
        else:
            relevant_dt = headers["anthropic-ratelimit-requests-reset"]

        try:
            reset_time = datetime.datetime.fromisoformat(relevant_dt)
        except ValueError:
            return datetime.timedelta(seconds=5)

        now = datetime.datetime.now(tz=zoneinfo.ZoneInfo("UTC"))
        return reset_time - now


__all__ = ["AnthropicClient"]
