
from typing import List, Dict
from utils.memory.memory_base import MemoryBase
from sqlmodel import Session

import db.svc
from db.engine import engine

class DBMessageMemory(MemoryBase):
    def __init__(self):
        super().__init__()
        self.chat_id = None
        self.message_id = None
        self.metainfo = None
        self.keywords = None

    def add_message(self, content: str, message_type: str = "user"):
        if message_type not in ["system", "user", "assistant"]:
            raise ValueError("message_type must be 'system', 'user', or 'assistant'")
        db.svc.insert_message(Session(engine), self.chat_id, content, self.message_id, message_type, self.metainfo,
                              self.keywords)

    def get_all_messages(self) -> List[Dict[str, str]]:
        converted_history = db.svc.find_chat_history(Session(engine), self.chat_id)
        return converted_history

    def get_past_messages(self) -> List[Dict[str, str]]:
        converted_history = db.svc.find_chat_history(Session(engine), self.chat_id)
        return converted_history
