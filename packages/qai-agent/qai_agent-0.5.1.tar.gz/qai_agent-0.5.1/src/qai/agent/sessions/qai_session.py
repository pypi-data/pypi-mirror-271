import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Optional

from llama_index.agent.openai import OpenAIAgent
from llama_index.core import SQLDatabase
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.memory.types import BaseMemory
from llama_index.core.query_engine import NLSQLTableQueryEngine
from qai.ai import MessageRole, QueryReturn, to_message
from qai.ai.frameworks.openai.llm import OpenAILLM
from sqlalchemy import create_engine

# from qai.qaibot.tools import Action, Step, fn_break_into_steps
# from qai.qaibot.utils.utils import modify_sql_query, refine_step_queries
from qai.agent.agents.find_agent import AgentType

tables = ["Companies", "Industries", "CompanyIndustries"]


@dataclass
class QaiSession(OpenAIAgent):
    db_config: dict
    model_config: dict
    session_id: str = None
    agent_type: AgentType = None
    messages: list[dict] = field(default_factory=list)
    user_id: str = None
    memory: BaseMemory = None

    def chat(self, query: str):
        self.memory.chat_store.add_message(
            key=self.user_id,
            message=ChatMessage(
                content=query,
                role=MessageRole.USER,
            ),
        )
        msgs = self.memory.chat_store.get_messages(self.user_id)
        msgs = [{"role": msg.role, "content": msg.content} for msg in msgs]
        llm = OpenAILLM(config=self.model_config)
        qr = llm.query(query, messages=msgs)

        self.memory.chat_store.add_message(
            key=self.user_id,
            message=ChatMessage(**qr.to_message()),
        )
