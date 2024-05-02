import os
import uuid
from abc import abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pprint import pprint
from typing import Any, Deque, Dict, List, Optional, Union, cast

import llama_index.core.instrumentation as instrument
from llama_index.agent.openai import OpenAIAgent
from llama_index.agent.openai.base import DEFAULT_MAX_FUNCTION_CALLS
from llama_index.agent.openai.step import OpenAIAgentWorker
from llama_index.core import PromptTemplate, Settings, SQLDatabase
from llama_index.core.agent.runner.base import AgentRunner
from llama_index.core.agent.types import (
    BaseAgent,
    BaseAgentWorker,
    Task,
    TaskStep,
    TaskStepOutput,
)
from llama_index.core.base.llms.types import (
    ChatMessage,
    ChatResponse,
    ChatResponseAsyncGen,
    ChatResponseGen,
    CompletionResponse,
    CompletionResponseAsyncGen,
    CompletionResponseGen,
    LLMMetadata,
    MessageRole,
)
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.callbacks import (
    CallbackManager,
    CBEventType,
    EventPayload,
    trace_method,
)
from llama_index.core.chat_engine.types import (
    AGENT_CHAT_RESPONSE_TYPE,
    AgentChatResponse,
    ChatResponseMode,
    StreamingAgentChatResponse,
)
from llama_index.core.instrumentation.events.agent import (
    AgentChatWithStepEndEvent,
    AgentChatWithStepStartEvent,
    AgentRunStepEndEvent,
    AgentRunStepStartEvent,
)
from llama_index.core.llms import ChatMessage
from llama_index.core.llms.llm import LLM
from llama_index.core.memory import BaseMemory, ChatMemoryBuffer
from llama_index.core.memory.chat_memory_buffer import ChatMemoryBuffer
from llama_index.core.memory.types import BaseMemory
from llama_index.core.objects.base import ObjectRetriever
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.query_pipeline import CustomQueryComponent
from llama_index.core.settings import Settings
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.tools import BaseTool, FunctionTool, QueryEngineTool
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from llama_index.core.tools.types import BaseTool, ToolMetadata
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.llms.openai import OpenAI
from llama_index.llms.openai.utils import OpenAIToolCall
from llama_index.tools.database import DatabaseToolSpec
from pi_conf import AttrDict, load_config
from pi_log import logs
from pydantic import BaseModel, Field
from qai.ai import MessageRole, QueryReturn, to_message
from qai.ai.frameworks.openai.llm import OpenAILLM
from sqlalchemy import create_engine

from qai.agent import ROOT_DIR, cfg
from qai.agent.agents.find_agent import AgentType, FindAgentWorker
from qai.agent.qaibot import QaiBot, QaiSession
from qai.agent.sessions.qai_session import QaiSession
from qai.agent.tools.types import StringEnum
from qai.agent.utils.utils import refine_step_queries

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.dirname(ROOT_DIR)))
# db_config = {"connect_str": f"sqlite:///{PROJ_DIR}/scripts/qrev-org-intel.merged.sqlite3"}
# print(db_config)
from llama_index.core.agent.runner.base import dispatcher

Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)


class StepModel(BaseModel):
    sentence: str = Field(
        description=(
            "A revised sentence that captures the business logic. the revised sentence keeps details such as numbers."
        )
    )
    category: str = Field(
        description="The category of the step, for example: company, people, etc."
    )

    # class Config:
    #     arbitrary_types_allowed = True
find_steps_description =     """
    Separate the text into a list of logical execution steps for a business user.
    The steps should be in the order of execution.
    Keep details such as quantities or numbers.
    Non business steps should be classified as extraneous.

    Args:
        steps (List[StepModel]): A list of StepModel objects, each containing a sentence and a category

    """
def find_steps(steps: list[StepModel]) -> QueryReturn:
    """
    Separate the text into a list of logical execution steps for a business user.
    The steps should be in the order of execution.
    Keep details such as quantities or numbers.
    Non business steps should be classified as extraneous.

    Args:
        steps (List[StepModel]): A list of StepModel objects, each containing a sentence and a category

    """
    print(f"steps = {steps}")
    for step in steps:
        # print(f"step = {step}")
        print(f"step.sentence = {step.sentence}")
        print(f"step.category = {step.category}")
    # q = self.query_engine.query(query)
    # print(f"q = {q}")
    return "" 
class SQLToolSpec(DatabaseToolSpec):
    """Simple Database tool."""

    ## List of tables in the database, None for all tables
    tables: Optional[list[str]] = None
    llm: Optional[LLM] = None
    refine_query_system_message: str = (
        "Separate the text into a list of logical execution steps for a business user and categorize the step."
        "The steps should be in the order of execution. "
        "Keep details such as quantities or numbers."
        "WHen choosing a category only use one of the following: {categories}"
        "For example if the user query is 'Get me the head of sales for the top 5 companies in the seattle area' and the following database schema {schema}, the refined query should be: "
        "step: Get the top 5 companies in the seattle area, category: company"
        "step: Get the head of sales for each company, category: people"
        ""
    )
    spec_functions = ["find_steps"]

    def __init__(self, llm: LLM = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.llm = llm
        # self.spec_functions.extend(self.extra_spec_functions)

    def query(self, query: str) -> QueryReturn:
        return self.query_engine.query(query)


    def refine_query(self, query: str) -> ChatResponse:
        """
        Refine the database query with schema information to make it more likely to have correct results. Returns the revised string query.

        Args:
            query (str): a sentence to be refined to be more suitable for sql queries

        Returns:
            ChatResponse: The refined query

        """
        tables = self.tables or self.list_tables()
        # categories = []
        # for table in tables:

        #     categories.append(f"table")
        #     for col in self.list_columns(table):
        #         categories.append(f"Column: {col}")

        schema_str = self.describe_tables()
        msgs = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=self.refine_query_system_message.format(
                    schema=schema_str, categories=tables
                ),
            ),
            ChatMessage(role=MessageRole.USER, content=query),
        ]

        return self.llm.chat(messages=msgs)


if __name__ == "__main__":
    cfg = load_config("qai-chat")
    # db_config = cfg["db"]

    # pprint(cfg.db)
    db_tools = SQLToolSpec(
        uri=cfg.db.uri,
    )

    query = "Get me the head of sales for the top 5 companies in the seattle area"
    #
    tool = FunctionTool.from_defaults(
            name="find_steps",
            fn=find_steps,
            tool_metadata=ToolMetadata(
                name="find_steps",
                description=find_steps_description,
                fn_schema=StepModel,
            ),
        )
    agent = OpenAIAgent.from_tools([tool], verbose=True)
    r = agent.chat(query)
    print("@@@@@@@@@")
    print(r)
    # agent = OpenAIAgent.from_tools(db_tools.to_tool_list(), verbose=True)
    # r = agent.chat(query)
    # # r = db_tools.refine_query(query)
    # print("@@@@@@@@@")
    # print(r)
    # engine = create_engine(cfg.db.uri)
    # tables = ["Companies", "Industries", "CompanyIndustries"]
    # if True:
    #     sql_database = SQLDatabase(engine, include_tables=tables)

    #     query_engine = NLSQLTableQueryEngine(
    #         sql_database=sql_database,
    #         tables=tables,
    #     )

    #     # print("****************")
    #     qr = query_engine.query(str(query))
    #     print("!!!!!!!!!!!!!!!!!!")
    #     print(qr)
    #     if qr.metadata and "sql_query" in qr.metadata:
    #         sql_query = qr.metadata["sql_query"]
    #         print("##", sql_query)

    #     # print(agent.chat(str(r)))
    # else:
    #     agent = OpenAIAgent.from_tools(db_tools.to_tool_list(), verbose=True)
    #     qr = agent.chat(str(r))
    # print("@@@@@@@@@")
    # print(qr)
