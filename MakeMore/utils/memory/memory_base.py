from abc import ABC, abstractmethod
from typing import List, Dict


class MemoryBase(ABC):
    def __init__(self):
        self.messages: List[Dict[str, str]] = []

    def add_message(self, content: str, message_type: str = "user"):
        if message_type not in ["system", "user", "assistant"]:
            raise ValueError("message_type must be 'system', 'user', or 'assistant'")
        self.messages.append({"role": message_type, "content": content})

    @abstractmethod
    def get_past_messages(self) -> List[Dict[str, str]]:
        """
        get past messages, it may be diff if using K, summary memory
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_messages(self) -> List[Dict[str, str]]:
        """
        get all past messages
        """
        raise NotImplementedError


class AllMessageMemory(MemoryBase):
    def __init__(self):
        super().__init__()

    def get_all_messages(self) -> List[Dict[str, str]]:
        return self.messages

    def get_past_messages(self) -> List[Dict[str, str]]:
        return self.messages.copy()


class KMessageMemory(MemoryBase):
    def __init__(self, k: int):
        super().__init__()
        self.k = k

    def get_all_messages(self) -> List[Dict[str, str]]:
        return self.messages

    def get_past_messages(self) -> List[Dict[str, str]]:
        n = len(self.messages)
        start_index = n - 2 * self.k
        start_index = max(1, start_index)
        result = [self.messages[0]] + self.messages[start_index:]
        return result


class ZeroMessageMemory(MemoryBase):
    def __init__(self):
        super().__init__()

    def get_past_messages(self) -> List[Dict[str, str]]:
        return [self.messages[0], self.messages[-1]] if self.messages else []

    def get_all_messages(self) -> List[Dict[str, str]]:
        return self.messages


class LLMSummaryMessageMemory(MemoryBase):
    def __init__(self):
        super().__init__()
