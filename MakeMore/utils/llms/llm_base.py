from abc import ABC, abstractmethod
from typing import List, Optional, Union, Dict, AsyncGenerator
from MakeMore.utils.memory.memory_base import MemoryBase
from typing import AsyncIterable
class LLMBase(ABC):
    def __init__(self, ):
        super().__init__()
        self.memory: Union[MemoryBase, None] = None

    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]], stop_words: Optional[List[str]] = None, stream=False) -> str:
        raise NotImplementedError

    @abstractmethod
    async def yield_chat(self, messages: List[Dict[str, str]], stop_words: Optional[List[str]] = None) -> AsyncIterable:
        raise NotImplementedError




