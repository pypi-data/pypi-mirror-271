import os
import re
import uuid
from abc import abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass, field
from inspect import signature
from llama_index.core.base.response.schema import Response
from pprint import pprint
from typing import (
    Any,
    Awaitable,
    Callable,
    Deque,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
    cast,
)

import llama_index.core.instrumentation as instrument
from llama_index.agent.openai import OpenAIAgent
from llama_index.agent.openai.base import DEFAULT_MAX_FUNCTION_CALLS
from llama_index.agent.openai.step import OpenAIAgentWorker
from llama_index.core import PromptTemplate, Settings, SQLDatabase
from llama_index.core.agent.runner.base import AgentRunner
from pydantic.type_adapter import TypeAdapter
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

# from pydantic.v1 import BaseModel, Field
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
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from llama_index.core.tools.types import BaseTool, ToolMetadata
from llama_index.core.tools.utils import create_schema_from_function
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.llms.openai import OpenAI
from llama_index.llms.openai.utils import OpenAIToolCall
from llama_index.tools.database import DatabaseToolSpec
from pi_conf import AttrDict, load_config
from pi_log import logs

from qai.ai import MessageRole, QueryReturn, to_message
from qai.ai.frameworks.openai.llm import OpenAILLM
from sqlalchemy import create_engine
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.schema import CreateTable

from qai.agent import ROOT_DIR, cfg
from qai.agent.agents.find_agent import AgentType, FindAgentWorker
from qai.agent.qaibot import QaiBot, QaiSession
from qai.agent.sessions.qai_session import QaiSession
from qai.agent.tools.types import StringEnum
from pydantic.tools import parse_obj_as

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.dirname(ROOT_DIR)))
import pydantic

# db_config = {"connect_str": f"sqlite:///{PROJ_DIR}/scripts/qrev-org-intel.merged.sqlite3"}
# print(db_config)
from llama_index.core.agent.runner.base import dispatcher

Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.0)



class PeopleIds(BaseModel):
    id : str = Field(..., description="The id of the person")

class CompanyIds(BaseModel):
    id : str = Field(..., description="The id of the company")

class IndustryIds(BaseModel):
    id : str = Field(..., description="The id of the industry")


class StepModel(BaseModel):
    sentence: str = Field(
        ...,
        description=(
            "A revised sentence that captures the business logic. the revised sentence keeps details such as numbers."
        ),
    )
    category: str = Field(
        ..., description="The category of the step, for example: company, people, etc."
    )

    class Config:
        arbitrary_types_allowed = True


class RefineSQLQuery(DatabaseToolSpec):
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
    spec_functions = ["find_steps", "load_data", "describe_tables", "list_tables"]

    def __init__(self, llm: LLM = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.llm = llm
        ## get columns from the database
        self.columns = self.list_tables
        # self.spec_functions.extend(self.extra_spec_functions)

    def tables_to_json(self, tables: Optional[List[str]] = None) -> dict:
        """
        Converts the specified tables in the database into a simple json format

        Args:
            tables (List[str]): A list of table names to retrieve details about
        """
        table_names = tables or [table.name for table in self._metadata.sorted_tables]
        json_tables = {}
        for table_name in table_names:
            columns = []
            table = next(
                (table for table in self._metadata.sorted_tables if table.name == table_name),
                None,
            )
            if table is None:
                raise NoSuchTableError(f"Table '{table_name}' does not exist.")
            schema = CreateTable(table).compile(self.sql_database._engine)
            try:
                for col in schema.statement.columns:
                    s = str(col).split(" ")
                    name = s[0].strip('"')
                    type = s[1]
                    columns.append({"name": name, "type": type})
            except:
                raise
            json_tables[table_name] = columns

        return json_tables

    def query(self, query: str) -> QueryReturn:
        return self.query_engine.query(query)

    def find_steps(self, steps: list[StepModel]) -> list[StepModel]:
        """
        Separate the text into a list of logical execution steps for a business user.
        The steps should be in the order of execution.
        Keep details such as quantities or numbers.
        Non business steps should be classified as extraneous.

        Args:
            steps (List[StepModel]): A list of StepModel objects, each containing a sentence and a category

        """
        ## Input is not perfect from the llm, it can be a list of steps but in dict form
        ## or it can be a dict with a list of dicts
        ## comes in as a list of steps but in dict form
        if isinstance(steps, dict):
            steps = steps["steps"]
        steps = [StepModel(**step) for step in steps]
        steps = self._refine_step_queries(steps)
        print(f"Returning steps = {steps}")
        return steps

    ## separate company and people steps. Merge filters into the same step.
    def _merge_steps(self, steps: list[StepModel]) -> list[StepModel]:
        """Merge the steps into a list of steps with the same category.

        Args:
            steps (list[dict[str, str]]): The list of steps to merge.

        Returns:
            list[dict[str, str]]: The merged list of steps.
        """
        new_steps: list[StepModel] = []
        old_category = None
        for step in steps:
            if old_category is None or old_category != step.category:
                new_steps.append(step)
            else:
                new_steps[-1].sentence += " " + step.sentence
            old_category = step.category
        return new_steps

    def _fix_proper_nouns(self, sentence: str) -> str:
        """
        Fix the proper nouns in the sentence by replacing them with the correct case from the database.

        Args:
            sentence (str): The sentence to fix.

        Returns:
            str: The fixed sentence.
        """
        ## Replace the potentially wrong case technology name with the correct case from the database
        # sentence = re.sub(tech, proper_name, sentence, re.IGNORECASE)
        return sentence

    def _refine_step_queries(self, steps: list[StepModel]) -> list[StepModel]:
        """
        Refine the step queries by replacing the technology names with the correct case from the database.

        Args:
            steps (list[StepModel]): The list of steps to refine.

        Returns:
            list[StepModel]: The refined list of steps.
        """

        steps = self._merge_steps(steps)
        return steps


    def load_people(self, query: str) -> List[PeopleIds]:
        """
        Load people from the database using the query.
        Args:
            query (str): Natural language of the query to load people from the database.
        Returns:
            List[PeopleIds]: A list of people ids.
        """



if __name__ == "__main__":
    cfg = load_config("qai-chat")
    # db_config = cfg["db"]

    # pprint(cfg.db)
    refine_tools = RefineSQLQuery(
        uri=cfg.db.uri, 
    )
    db_tools = DatabaseToolSpec(
        uri=cfg.db.uri,
    )

    query = "Get me the head of sales for the top 5 companies in the seattle area"
    query += "Only use the tool 'find_steps' to refine the query."
    # # #
    # tools = db_tools.to_tool_list()
    # # # pprint(tools[0].metadata.to_openai_function())
    refining_agent = OpenAIAgent.from_tools(refine_tools.to_tool_list(), verbose=True)
    r = refining_agent.chat(query, tool_choice="find_steps")
    # r = agent.run_step()
    # # # # r = db_tools.refine_query(query)
    print("@@@@@@@@@")
    print(r)
    print("!!!!!!!!!!!!!!!!!!")
    query2_list = []
    try:
        source = r.sources[-1]
        for raw_output in source.raw_output:
            print("   ###########")
            sm: StepModel = raw_output
            query2_list.append(sm.sentence)
        query2 = " ".join(query2_list)
    except:
        raise
    # query2 = " ".join([s["sentence"] for s in r.sources if r.category != "extraneous"])
    # agent = OpenAIAgent.from_tools(db_tools.to_tool_list(), verbose=True)
    print(f" ###### Q2 = {query2} ######")
    engine = create_engine(cfg.db.uri)
    tables = ["Companies", "Industries", "CompanyIndustries", "People"]

    sql_database = SQLDatabase(engine, include_tables=tables)

    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=tables,
    )
    query2 += "return all the information using '*' in the resulting sql query"
    r2: Response = query_engine.query(str(query2))
    # r2 = agent.chat(query2)

    print("@@@@@@@@@")
    print(r2)
    print("!!!!!!!!!!!!!!!!!!")
    sql_query = None
    if r2.metadata and "sql_query" in r2.metadata:
        sql_query = r2.metadata["sql_query"]
        print("##", sql_query)

    # r3 = agent.chat("actually, I want to see 5 different companies")
    # print("@@@@@@@@@ R3")
    # print(r3)
    # print("!!!!!!!!!!!!!!!!!!")
    print("@*#*#*# DONE @*#*#*#")
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
