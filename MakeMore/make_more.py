from typing import List, Dict
from MakeMore.utils.llms.openai_SDK import OpenAI_LLM
from MakeMore.utils.memory.memory_base import AllMessageMemory
from MakeMore.utils.utils import *
from pprint import pprint
import asyncio
from tqdm.asyncio import tqdm
import base64
import os


class MakeMoreAgent:
    def __init__(
            self,
            llm_configs,
            system_prompt
    ) -> None:
        self.system_prompt = system_prompt
        self.llm = OpenAI_LLM(
            temp=llm_configs.get("temp", 0.7),
            topp=llm_configs.get("topp", 0.9),
            model_name=llm_configs.get("model_name", ""),
            url=llm_configs.get("base_url", ""),
            key=llm_configs.get("key", ""),
            stop_words=llm_configs.get("stop_words", [])
        )
        self.memory = AllMessageMemory()
        self.memory.add_message(system_prompt, message_type="system")

    async def chat(self,query:str):
        messages = self.memory.get_all_messages()[:]
        messages.append({"role":"user","content":query})
        summary_res = ""
        async for char in self.llm.yield_chat(messages=messages):
            summary_res += char
            
        return summary_res

    def _encode_image_to_base64(self, image_path: str) -> str:
        """Convert image to base64 encoding"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    async def mm_chat(self, query: str, image_path: str = None):
        """Multimodal chat with text and optional image"""
        messages = self.memory.get_all_messages()[:]
        
        if image_path and os.path.exists(image_path):
            base64_image = self._encode_image_to_base64(image_path)
            content = [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                {"type": "text", "text": query}
            ]
            messages.append({"role": "user", "content": content})
        else:
            # Regular text message
            messages.append({"role": "user", "content": query})
            
        summary_res = ""
        async for char in self.llm.yield_chat(messages=messages):
            summary_res += char
            
        return summary_res

    async def batch_chat(self, queries: list[str], batch_size: int = 5) -> list:
        """批量处理查询请求，并允许动态填充任务"""
        results = [None] * len(queries)
        semaphore = asyncio.Semaphore(batch_size)  

        async def process_single_query(query: str, index: int):
            async with semaphore:  #
                results[index] = await self.chat(query)

        # 使用 create_task 启动所有任务，并且动态管理
        tasks = [asyncio.create_task(process_single_query(query, i)) for i, query in enumerate(queries)]

        # tqdm.as_completed() 可以动态更新进度
        for task in tqdm(asyncio.as_completed(tasks), total=len(queries), desc="processing"):
            await task  # 确保任务完成

        return results
    
    async def mm_batch_chat(self, queries: List[Dict[str, str]], batch_size: int = 5) -> list:
        """批量处理多模态查询请求
        
        Args:
            queries: 格式为 [{"question": "问题内容", "image_url": "本地图片路径"}, ...]
            batch_size: 并发处理的批次大小
            
        Returns:
            包含所有响应的列表
        """
        results = [None] * len(queries)
        semaphore = asyncio.Semaphore(batch_size) 

        async def process_single_query(query_data: Dict[str, str], index: int):
            async with semaphore:  # 进入时获取信号量，退出时自动释放
                question = query_data.get("question", "")
                image_url = query_data.get("image_url", None)
                results[index] = await self.mm_chat(question, image_url)

        tasks = [asyncio.create_task(process_single_query(query, i)) for i, query in enumerate(queries)]

        for task in tqdm(asyncio.as_completed(tasks), total=len(queries), desc="processing multimodal queries"):
            await task  

        return results

        


if __name__ == "__main__":
    llm_configs = {
        "temp": 0.7,
        "topp": 0.9,
        "model_name": "Chat",
        "base_url": "yours",
        "key": "EMPTY",
        "stop_words": []
    }
    
    system_prompt = """你是一个乐于助人的AI助手
    """
    
    mma = MakeMoreAgent(llm_configs, system_prompt)
    
    async def main():
        test_query = "我国国土面积比澳大利亚大多少"
        result = await mma.chat(test_query)
        pprint(result)
        
        # 测试批量查询
        test_queries = [
            "中国的人口有多少",
            "北京的面积是多少",
            "上海有多少区",
        ]
        batch_results = await mma.batch_chat(test_queries, batch_size=3)
        pprint(batch_results)
        
        # 测试多模态查询
        test_mm_query = "这张图片是什么？"
        test_image_path = "t2.png"
        mm_result = await mma.mm_chat(test_mm_query, test_image_path)
        pprint(mm_result)
        
        # 测试多模态批量查询
        test_mm_queries = [
            {"question": "这张图片是什么？", "image_url": "t2.png"},
            {"question": "这张图片是什么？", "image_url": "t2.png"},
            {"question": "这张图片是什么？", "image_url": "t2.png"},
        ]
        mm_batch_results = await mma.mm_batch_chat(test_mm_queries, batch_size=2)
        pprint(mm_batch_results)

    # 运行测试
    asyncio.run(main())
