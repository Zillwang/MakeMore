from loguru import logger
from openai import AsyncOpenAI
from typing import List, Optional, Dict, AsyncIterable
from MakeMore.utils.llms.llm_base import LLMBase

class OpenAI_LLM(LLMBase):
    def __init__(
        self,
        temp: float,
        topp: float,
        model_name: str = "",
        url: str="",
        key:str = "",
        stop_words = [],
    ):
        super().__init__()
        self.stream = None
        
        self.temp = temp
        self.topp = topp
        self.model_name = model_name
        self.base_url = url
        self.key = key
        self.stop_words = stop_words
        print(self.base_url)
        print(self.key)
        self.client = AsyncOpenAI(
            api_key=self.key,
            base_url=self.base_url
        )        
    async def yield_openai_call(self, messages, stop_words):
        result = await self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temp,
            top_p=self.topp,
            messages=messages,
            stop=stop_words,
            stream=True,
            frequency_penalty=0.05,
            max_tokens=4096,
        )
        # logger.info("---------------------yield_openai_call 调用openai---------------------")

        full_response = ""
        async for chunk in result:
            if chunk is not None and chunk.choices[0].delta.content is not None:
                char = chunk.choices[0].delta.content
                full_response += char
                yield char


    async def yield_chat(self, messages: List[Dict[str, str]], stop_words: Optional[List[str]] = None) -> AsyncIterable[str]:
        result = await self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temp,
            top_p=self.topp,
            messages=messages,
            stop=stop_words,
            stream=True,
            frequency_penalty=0.05,
            max_tokens=4096,
        )
        # logger.info("---------------------yield_openai_call 调用openai---------------------")
        async for chunk in result:
            if chunk is not None and chunk.choices[0].delta.content is not None:
                char = chunk.choices[0].delta.content
                yield char

    async def chat(self, messages: List[Dict[str, str]], stop_words: Optional[List[str]] = None, stream=False):
        self.stream = stream

        result = await self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temp,
            top_p=self.topp,
            messages=messages,
            stop=stop_words,
            stream=self.stream,
            frequency_penalty=1.05,
            max_tokens=4096,
        )
        # logger.info(f"---------------------openai_call 调用openai {messages}---------------------")
        if self.stream:
            response = ""
            async for chunk in result:
                if chunk is not None:
                    char = chunk.choices[0].delta.content
                    if char:
                        logger.info(char, end="")
                        response += char
            print()
            return response
        else:
            return result.choices[0].message.content

