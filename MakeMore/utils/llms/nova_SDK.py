from datetime import datetime
from typing import List, Optional, AsyncGenerator, Dict
from typing import List, Optional, Generator

from loguru import logger
from openai import OpenAI

# from prompts.summary_prompts import search_summary_system_prompt_zh
from typing import List, Optional, Generator
from MakeMore.utils.llms.llm_base import LLMBase
import sensenova
from datetime import datetime


class Nova_LLM(LLMBase):
    def __init__(self, model_name: str, temp: float, topp: float, memory=None):
        super().__init__()
        self.stream = None
        self.model_name = model_name
        self.temp = temp
        self.topp = topp
        self.memory = memory
        self.client = self.init_nova_clients()

    def init_nova_clients(self):
        clients = {
            "SenseChat-5": ("access_key_id", "secret_access_key"),
            "SenseChat-128K": ("access_key_id", "secret_access_key"),
            "SenseChat-Turbo": ("access_key_id", "secret_access_key"),
        }
        if self.model_name not in clients:
            raise ValueError("Model name not supported")

        access_key_id, secret_access_key = clients[self.model_name]
        sensenova.access_key_id = self.config[access_key_id]
        sensenova.secret_access_key = self.config[secret_access_key]
        return sensenova

    async def yield_nova_call(self, messages, stop_words):
        result = await sensenova.ChatCompletion.acreate(
            messages=messages,
            model=self.model_name,
            stream=True,
            max_new_tokens=1024,
            repetition_penalty=1.05,
            temperature=self.temp,
            top_p=self.topp,
        )

        full_response = ""
        async for part in result:
            choices = part["data"]["choices"]
            for c_idx, c in enumerate(choices):
                delta = c.get("delta")
                if delta:
                    char = delta
                    full_response += char
                    yield char

        # for chunk in result:
        #     if chunk is not None and chunk.choices[0].delta.content is not None:
        #         char = chunk.choices[0].delta.content
        #         full_response += char
        #         yield char

    async def yield_chat(self, query: str, stop_words: Optional[List[str]] = None) -> Generator[str, None, None]:
        if self.memory:
            messages = self.memory.get_past_messages()
            messages[0] = {"role": "system", "content": messages[0]["content"].format(
                formatted_date=datetime.now().strftime("%Y-%m-%d %H:%M"))}
            messages.append({"role": "user", "content": query})
        else:
            messages = [{"role": "user", "content": query}]

        response_generator = self.yield_nova_call(messages, stop_words)
        full_response = ""
        async for chunk in response_generator:
            full_response += chunk
            yield chunk
        self.memory.add_message(self.truncate_string(query), "user")
        self.memory.add_message(full_response, "assistant")

    # async def yield_chat_from_db(self, query: str, stop_words: Optional[List[str]] = None,
    #                              guiding_res: Optional[str] = None) -> AsyncGenerator[str, None]:
    #     messages = self.memory.get_past_messages()
    #     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     summary_system_prompt = search_summary_system_prompt_zh.format(
    #         formatted_date=now)
    #     # logger.info(f"now:   {now}")
    #     messages.insert(0, {"role": "system", "content": summary_system_prompt})
    #     messages.append({"role": "user", "content": query})
    #     logger.info(f"messages:   {messages}")
    #
    #     response_generator = self.yield_nova_call(messages, stop_words)
    #     full_response = ""
    #     for guiding_res_chunk in guiding_res:
    #         full_response += guiding_res_chunk
    #         yield guiding_res_chunk
    #     async for chunk in response_generator:
    #         full_response += chunk
    #         yield chunk
    #     # self.memory.add_message(self.truncate_string(query), "user")
    #     # self.memory.add_message(full_response, "assistant")

    async def yield_chat_from_db(self, messages: List[Dict[str, str]], stop_words: Optional[List[str]] = None,
                                 guiding_res: Optional[str] = None) -> AsyncGenerator[str, None]:

        response_generator = self.yield_nova_call(messages, stop_words)
        full_response = ""
        for guiding_res_chunk in guiding_res:
            full_response += guiding_res_chunk
            yield guiding_res_chunk
        async for chunk in response_generator:
            full_response += chunk
            yield chunk

    async def nova_call(self, messages, stop_words):
        # print(messages)
        result = await sensenova.ChatCompletion.acreate(
            messages=messages,
            model=self.model_name,
            stream=self.stream,
            max_new_tokens=1024,
            repetition_penalty=1.05,
            temperature=self.temp,
            top_p=self.topp,
        )
        if self.stream:
            response = ""
            for part in result:
                choices = part["data"]["choices"]
                for c_idx, c in enumerate(choices):
                    delta = c.get("delta")
                    if delta:
                        print(delta, end="")
                        response += delta
            print()
            return response
        else:
            return result["data"]["choices"][0]["message"]

    # async def chat(self, query: str, stop_words: Optional[List[str]] = None, stream=False):
    #     self.stream = stream
    #     if self.memory:
    #         messages = self.memory.get_past_messages()
    #         # print(messages)
    #         messages[0] = {"role": "system", "content": messages[0]["content"].format(
    #             formatted_date=datetime.now().strftime("%Y-%m-%d %H:%M"))}
    #         messages.append({"role": "user", "content": query})
    #         response = await self.nova_call(messages, stop_words)
    #         self.memory.add_message(self.truncate_string(query), "user")
    #         self.memory.add_message(response, "assistant")
    #     else:
    #         response = await self.nova_call([{"role": "user", "content": query}], stop_words)
    #     return response

    async def chat(self, messages: List[Dict[str, str]], stop_words: Optional[List[str]] = None, stream=False):
        self.stream = stream

        response = await self.nova_call(messages, stop_words)
        # logger.info(f"response:   {response}")
        return response
