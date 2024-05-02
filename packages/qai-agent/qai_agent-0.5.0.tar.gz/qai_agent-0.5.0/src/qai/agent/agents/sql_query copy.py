import os
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from llama_index.agent.openai import OpenAIAgent
from llama_index.agent.openai.base import DEFAULT_MAX_FUNCTION_CALLS
from llama_index.agent.openai.step import OpenAIAgentWorker
from llama_index.core import SQLDatabase
from llama_index.core.agent.runner.base import AgentRunner
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.callbacks import CallbackManager
from llama_index.core.llms import ChatMessage
from llama_index.core.llms.llm import LLM
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.memory.chat_memory_buffer import ChatMemoryBuffer
from llama_index.core.memory.types import BaseMemory
from llama_index.core.objects.base import ObjectRetriever
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.query_pipeline import CustomQueryComponent
from llama_index.core.settings import Settings
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.tools import BaseTool, FunctionTool, QueryEngineTool
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from llama_index.core.tools.types import ToolMetadata
from llama_index.llms.openai import OpenAI
from llama_index.llms.openai.utils import OpenAIToolCall
from llama_index.tools.database import DatabaseToolSpec
from pi_conf import AttrDict, load_config
from pi_log import logs
from pydantic import BaseModel, Field
from qai.ai import MessageRole, QueryReturn, to_message
from qai.ai.frameworks.openai.llm import OpenAILLM
from sqlalchemy import create_engine

# tables = ["Companies", "Industries", "CompanyIndustries"]
# engine = create_engine(self.db_config["connect_str"])
from qai.agent import ROOT_DIR, cfg
from qai.agent.agents.find_agent import AgentType, FindAgentWorker
from qai.agent.qaibot import QaiBot, QaiSession
from qai.agent.sessions.qai_session import QaiSession
from qai.agent.tools.types import StringEnum

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.dirname(ROOT_DIR)))
# db_config = {"connect_str": f"sqlite:///{PROJ_DIR}/scripts/qrev-org-intel.merged.sqlite3"}
# print(db_config)


    # (
    #     "Given a database schema and a user query, "
    #     "break down the query into a series of logical steps expressed in natural language, "
    #     "rather than directly translating it into SQL commands. "
    #     "Request id's rather than entire objects"
    #     "Schema:\n{schema}\n"
    # )

    # extra_spec_functions: list[str] = ["refine_query"]


class SQLToolSpec(BaseToolSpec):
    name: str = "sql_query"
    description: str = "A tool for querying SQL databases."
    spec_functions: list[str] = ["query"]

    def __init__(self, db_config: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_config = db_config
        # self.engine = create_engine(self.db_config["connect_str"])
        # self.query_engine = NLSQLTableQueryEngine(engine=self.engine, tables=tables)

    def query(self, query: str) -> QueryReturn:
        return self.query_engine.query(query)


from enum import StrEnum
from typing import Self


class Step(StrEnum):
    create_campaign = "create_campaign"
    company_list = "company_list"
    company_filter = "company_filter"
    company_more_info = "company_more_info"
    people_list = "people_list"
    people_filter = "people_filter"
    people_more_info = "people_more_info"
    industry_list = "industry_list"
    industry_filter = "industry_filter"
    industry_more_info = "industry_more_info"
    action_email = "action_email"
    action_sms = "action_sms"
    action_call = "action_call"
    action_reminder = "action_reminder"
    action_graph_results = "action_graph_results"
    action_table_results = "action_table_results"
    more_info = "more_info"
    extraneous = "extraneous"


fn_break_into_steps = {
    "type": "function",
    "function": {
        "name": "break_into_steps",
        "description": (
            "Separate the text into a list of logical execution steps for a business user. "
            "The steps should be in the order of execution. "
            "Keep details such as quantities or numbers."
            "Non business steps should be classified as extraneous. "
            f"Categories should only be one of [{','.join([str(e) for e in Step])}]"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "sentence": {
                                "type": "string",
                                "description": (
                                    "A revised sentence that can be used for the steps, "
                                    "the revised sentence keeps details such as numbers."
                                ),
                            },
                            "category": {
                                "type": "string",
                                "enum": [str(e) for e in Step],
                                "description": "A category for the revised sentence. Describes whether the sentence is about companies, people, industries, or an action.",
                            },
                        },
                    },
                    "description": "The sentence that describes the step",
                },
            },
            "required": ["steps", "sentence", "category"],
        },
    },
}

if __name__ == "__main__":
    cfg = load_config("qai-chat")
    # db_config = cfg["db"]
    from pprint import pprint

    from qai.agent.utils.utils import refine_step_queries

    pprint(cfg.db)
    db_tools = DatabaseToolSpec(
        uri=cfg.db.uri
        # scheme="postgresql",  # Database Scheme
        # host="localhost",  # Database Host
        # port="5432",  # Database Port
        # user="postgres",  # Database User
        # password="FakeExamplePassword",  # Database Password
        # dbname="postgres",  # Database Name
    )

    # print(db_tools.describe_tables())
    prompt = f"Given this sentence: 'Get me the head of sales for the top 5 companies in the seattle area' and the following database schema {db_tools.describe_tables()}, revise the sentence into steps."
    agent = OpenAIAgent.from_tools(db_tools.to_tool_list(), verbose=True)
    # llm = OpenAILLM(config=cfg.model)
    # msgs = [
    #     {
    #         # "content": "What tables does this database contain",
    #         # "content": "Get me the head of sales for the top 5 companies in the seattle area",
    #         "content": prompt,
    #         "role": "user",
    #     },
    # ]
    # print(msgs)
    # qr = llm.query(
    #     messages=msgs,
    #     # tools=[fn_break_into_steps],
    #     # tool_choice="auto",
    #     # validate=True,
    #     # required_fields=["steps"],
    # )
    # print(qr.response)
    r = agent.chat("Get me the head of sales for the top 5 companies in the seattle area")
    for n in r.source_nodes:
        print(n)
    for n in r.sources:
        print(n)
    print("########")
    r = agent.chat("filter by people that only have 'r' in their name")
    print(r)
    print("@@@@@@@@@@@")
    # print(agent.chat(qr.response))
    # refined_steps = refine_step_queries(qr.arguments()["steps"])

    # for step, sentence in refined_steps:
    #     print(f"\t\tStep: {step}, Sentence: {sentence}")
    #     print(agent.chat(sentence))
    #     break
    # print(agent.chat("What tables does this database contain"))
    # # print( agent.chat("Describe the first table"))
    # # print(agent.chat("Retrieve the first row of that table"))





if __name__ == "__main__":
    cfg = load_config("qai-chat")
    # db_config = cfg["db"]
    from pprint import pprint

    from qai.agent.utils.utils import refine_step_queries

    # pprint(cfg.db)
    db_tools = SQLToolSpec(
        uri=cfg.db.uri,
        llm=OpenAI(cfg.model.name),
        # scheme="postgresql",  # Database Scheme
        # host="localhost",  # Database Host
        # port="5432",  # Database Port
        # user="postgres",  # Database User
        # password="FakeExamplePassword",  # Database Password
        # dbname="postgres",  # Database Name
    )

    # print(db_tools.describe_tables())
    # prompt = f"Given this sentence: 'Get me the head of sales for the top 5 companies in the seattle area' and the following database schema {db_tools.describe_tables()}, revise the sentence into steps."
    query = "Get me the head of sales for the top 5 companies in the seattle area"
    r = db_tools.refine_query(query)
    print("@@@@@@@@@")
    print(r)
    engine = create_engine(cfg.db.uri)
    tables = ["Companies", "Industries", "CompanyIndustries"]
    if True:
        sql_database = SQLDatabase(engine, include_tables=tables)

        query_engine = NLSQLTableQueryEngine(
            sql_database=sql_database,
            tables=tables,
        )

        # print("****************")
        qr = query_engine.query(str(query))
        print("!!!!!!!!!!!!!!!!!!")
        print(qr)
        if qr.metadata and "sql_query" in qr.metadata:
            sql_query = qr.metadata["sql_query"]
            print("##", sql_query)

        # print(agent.chat(str(r)))
    else:
        agent = OpenAIAgent.from_tools(db_tools.to_tool_list(), verbose=True)
        qr = agent.chat(str(r))
    print("@@@@@@@@@")
    print(qr)


# class RefineModel(BaseModel):
#     sentence: str = Field(description="The user sentence to find the correct agent for.")
#     agent_type: AgentType = Field(description="Which agent the user action belongs to.")
# model = "Writer/camel-5b-hf"
model = "JosephusCheung/LL7M"
# Settings.llm = HuggingFaceLLM(
#     context_window=2048,
#     max_new_tokens=256,
#     generate_kwargs={"temperature": 0.25, "do_sample": False},
#     # query_wrapper_prompt=query_wrapper_prompt,
#     tokenizer_name=model,
#     model_name=model,
#     device_map="auto",
#     tokenizer_kwargs={"max_length": 2048},
#     # uncomment this if using CUDA to reduce memory usage
#     # model_kwargs={"torch_dtype": torch.float16}
# )


# class RefineSQLRunner(AgentRunner):
#     @dispatcher.span
#     async def _achat(
#         self,
#         message: str,
#         chat_history: Optional[List[ChatMessage]] = None,
#         tool_choice: Union[str, dict] = "auto",
#         mode: ChatResponseMode = ChatResponseMode.WAIT,
#     ) -> AGENT_CHAT_RESPONSE_TYPE:

#         return
