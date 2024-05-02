import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from enum import StrEnum
from functools import partial
from typing import Any, Dict, List, Optional, Self, Sequence, Type, TypeVar, Union

import requests
from llama_index.agent.openai import OpenAIAgent
from llama_index.agent.openai.base import DEFAULT_MAX_FUNCTION_CALLS
from llama_index.agent.openai.step import OpenAIAgentWorker
from llama_index.core import SQLDatabase
from llama_index.core.agent import AgentChatResponse, Task
from llama_index.core.agent.runner.base import AgentRunner
from llama_index.core.agent.types import Task
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.callbacks import CallbackManager
from llama_index.core.chat_engine.types import AgentChatResponse
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
from llama_index.core.tools.types import BaseTool, ToolMetadata
from llama_index.llms.openai import OpenAI
from llama_index.llms.openai.utils import OpenAIToolCall
from pi_conf import AttrDict, load_config
from pi_log import logs
from pymongo import MongoClient
from qai.ai import MessageRole, QueryReturn, to_message
from qai.ai.frameworks.openai.llm import OpenAILLM
from sqlalchemy import create_engine

from qai.agent import cfg
from qai.agent.agents.find_agent import AgentType, FindAgentWorker
from qai.agent.agents.sql_query import RefineSQLQuery, StepModel
from qai.agent.agents.email import EmailModel, EmailAgent
from qai.agent.agents.tools.outreach import OutreachToolSpec
from qai.agent.models import OutreachType
from qai.agent.qaibot import QaiSession
from qai.agent.sessions.qai_session import QaiSession
from qai.agent.tools.types import StringEnum
from qai.agent.utils.distribute import adistribute


class PersonID(BaseModel):
    id: str = Field(description="The database id of the person.")


class PersonModel(BaseModel):
    id: Optional[str] = Field(description="The database id of the person.")
    name: Optional[str] = Field(description="The name of the person.")
    email: Optional[str] = Field(description="The email of the person.")
    phone: Optional[str] = Field(description="The phone number of the person.")
    linkedin: Optional[str] = Field(description="The linkedin profile of the person.")
    whatsapp: Optional[str] = Field(description="The whatsapp number of the person.")


class CompanyCampaignModel(BaseModel):
    people: list[str] = Field(description="A list of people to generate a campaign for.")
    companies: list[str] = Field(description="A list of companies to generate a campaign for.")
    outreach_types: list[OutreachType] = Field(
        description="The type of outreach to use for the campaign."
    )


class CampaignToolSpec(BaseToolSpec):
    agent: "CampaignAgent" = None
    companies: list[str] = Field(description="A list of companies to generate a campaign for.")
    spec_functions = ["create_campaign", "text_to_outreach_type"]

    def __init__(self, *args, **kwargs):
        pass

    def text_to_outreach_type(self, outreach_types: list[OutreachType]) -> list[OutreachType]:
        """
        Convert a natural langague of strings to a list of OutreachType objects.
        Args:
            outreach_types: A list of strings representing the outreach types.
        Returns:
            A list of OutreachType objects.
        """
        print(f"Converting outreach types: {outreach_types}")
        return outreach_types

    def create_campaign(
        self,
        people: list[PersonID],
        outreach_types: list[OutreachType],
    ) -> str:
        """
        Create a campaign for a list of PersonID objects. These id's should never be inferred.
        If they are missing, ask for them.
        Args:
            people: A list of PersonID objects to generate a campaign for.
            outreach_types: A list of OutreachType objects for how to contact the people.
        Returns:
            A string indicating the campaign was created.
        """
        # people = self.people
        print(
            f"Creating campaign for # people: {len(people)}  # outreach_types: {len(outreach_types)}, people={people}"
        )
        for p in people:
            print(f"Person: {p} Outreach: {outreach_types}")

        return "Campaign is starting to be created, it can be found in the campaign tab."


@dataclass
class CampaignResponse(AgentChatResponse):
    completed: bool = False
    emails: List[EmailModel] = None


class CampaignAgent(OpenAIAgent):
    """
    An agent that generates a campaign for a list of people and companies.
    """

    def __init__(self, tools: List[BaseTool], **kwargs: Any) -> None:
        """Init params."""
        super().__init__(
            tools=tools,
            **kwargs,
        )
        # The person to send the emails from.
        self.from_person: dict = {}
        # The company to send the emails from.
        self.from_company: dict = {}
        # A dict of people to generate a campaign for.
        self.people: dict = {}
        # A dict of companies to generate a campaign for.
        self.companies: dict = {}
        # The type of outreach to use for the campaign.
        self.outreach_types: list[OutreachType] = [OutreachType.email]
        # The URL to call when the emails are completed.
        self.on_complete_emails_url: Optional[str] = None

        self.email_agent: EmailAgent = None

    @staticmethod
    def _email_on_complete(url: str = None) -> None:
        print(f"Call sent to {url}")

    def _initialize_state(self, task: Task, **kwargs: Any) -> Dict[str, Any]:
        """Initialize state."""
        print(f"Initializing state for task {task} with kwargs {kwargs}")
        return {"count": 0, "current_reasoning": []}

    def chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        tool_choice: Optional[Union[str, dict]] = None,
    ) -> CampaignResponse:
        """
        Chat with the agent.
        """
        print(f"Chatting with message {message} and tool_choice {tool_choice}")
        print(
            f"  People IDs: {len(self.people)}, company IDs: {len(self.companies)}, "
            f"outreach types: {len(self.outreach_types)}"
        )

        # host (Optional[str]): host of the database connection.
        # port (Optional[int]): port of the database connection.
        # user (Optional[str]): user of the database connection.
        # password (Optional[str]): password of the database connection.

        refine_tools = RefineSQLQuery(**cfg.db)

        refining_agent = OpenAIAgent.from_tools(
            refine_tools.to_tool_list(),
            verbose=True,
            system_prompt=refine_tools.refine_query_system_message,
        )
        r: AgentChatResponse = refining_agent.chat(message, tool_choice="find_steps")
        if r.sources and r.sources[0].tool_name == "find_steps":
            tool = r.sources[0]
            steps: list[StepModel] = tool.raw_output
            print(f"  Tool output: ")
            for step in steps:
                try:
                    if step.category == "people":
                        result = refine_tools.load_people(step.sentence)
                        ## result is a list of dict, change to dict
                        if result:
                            result = {r["id"]: r for r in result}
                        self.people.update(result)
                        print(f"  Added People: {len(result)}")
                    elif step.category == "company":
                        result = refine_tools.load_companies(step.sentence)
                        ## result is a list of dict, change to dict
                        if result:
                            result = {r["id"]: r for r in result}
                        self.companies.update(result)
                        print(f"  Added Companies: {len(result)}")

                    else:
                        result = "No Result"
                except Exception as e:
                    print(f"Error: {e}\nStep={step}\nResult: {result}")
                    raise
                print(f"  Result: {result}")
        npeople = len(self.people) > 0
        ncompanies = len(self.companies) > 0
        noutreach = len(self.outreach_types) > 0
        assistant_message = ". I have the following:"
        if npeople:
            assistant_message += f"\n  People: {list(self.people.keys())[0]}"
        if ncompanies:
            assistant_message += f"\n  Companies: {list(self.companies.keys())[0]}"
        if noutreach:
            assistant_message += (
                f"\n  Outreach types: {' '.join([str(o) for o in self.outreach_types])}"
            )
        ## I am missing the following
        if not npeople or not noutreach:
            assistant_message += "\n. I am missing the following information :"
            if not npeople:
                assistant_message += "\n    People"
            ## Purposefully not using companies as we don't really need them
            if not noutreach:
                assistant_message += "\n    Outreach types"
        message += assistant_message
        response: AgentChatResponse = super().chat(message, chat_history, tool_choice)
        completed = response.sources and response.sources[0].tool_name == "create_campaign"
        setattr(response, "completed", completed)
        emails = None
        sequence_id = str(uuid.uuid4())

        if completed:
            emails = self.email_agent.create_emails(
                sequence_id, self.from_person, self.from_company, self.people, self.companies
            )
        setattr(response, "emails", emails)
        print(f"campaignagent::Chat completed={completed}  response: {response} emails: {emails}")
        return response

    def _finalize_task(self, task: Task, **kwargs: Any) -> None:
        """Finalize task."""
        print(f"Finalizing task with state {task} and kwargs {kwargs}")
        # nothing to finalize here

    @staticmethod
    def create(
        people: list[dict] = None,
        companies: list[dict] = None,
        outreach_types: list[OutreachType] = None,
        on_complete_emails_url: str = None,
        tools: List[BaseTool] = None,
        verbose: bool = False,
        from_company: dict = None,
        from_person: dict = None,
        model_config: dict = None,
        system_prompt: str = None,
        email_agent: EmailAgent = None,
        **kwargs,
    ) -> Self:
        campaign_tool = CampaignToolSpec()
        tools = tools or campaign_tool.to_tool_list()
        system_prompt = system_prompt or (
            "Create a campaign for a list of people and companies. If a parameter is missing,"
            " please ask for it, do not try to infer it."
        )
        agent: CampaignAgent = CampaignAgent.from_tools(
            tools=tools,
            system_prompt=system_prompt,
            verbose=verbose,
            **kwargs,
        )
        agent.people = people or {}
        agent.companies = companies or {}
        agent.on_complete_emails_url = on_complete_emails_url
        agent.from_person = from_person or {}
        agent.from_company = from_company or {}
        agent.email_agent = email_agent or EmailAgent.create(
            agent.from_person,
            agent.from_company,
        )
        return agent


if __name__ == "__main__":
    from pprint import pprint

    from pi_conf import AttrDict, load_config

    cfg = load_config("qai")
    cfg.to_env()
    # Create a new CampaignToolSpec object
    campaign_tool = CampaignToolSpec(companies=["Apple", "Google", "Microsoft"])
    # find_outreach_tool = OutreachToolSpec()
    # pprint(campaign_tool.to_tool_list()[0].metadata.to_openai_function())
    tools = campaign_tool.to_tool_list()

    agent = CampaignAgent.from_tools(
        tools=tools,
        system_prompt=(
            "Create a campaign for a list of people and companies. If a parameter is missing, please ask for it, do not try to infer it."
        ),
        verbose=True,
    )
    # llm = OpenAI(model="gpt-3.5-turbo", temperature=0.0)
    # OpenAIAgent
    # agent = OpenAIAgent(llm=llm, callback_manager=llm.callback_manager)
    r = agent.chat("Make an email campaign ")
    # pprint(r)
    # r = agent.chat("Sure, send them emails")
    pprint(r)
    r = agent.chat("Umm, to 5 of the some heads of companies around las vegas")
    pprint(r)
    print("DONE")
    # from qai.ai.frameworks.openai.llm import OpenAILLM
    # llm = OpenAILLM(config={"name":"gpt-3.5-turbo", "temperature":0.0})
    # msgs = [
    #     {"role": "system", "content": "Create a campaign for a list of people and companies. If a parameter is missing, please ask for it, do not try to infer it."},
    #     {"role": "user", "content": "Make a campaign "},
    # ]
    # msgs = [m.dict() for m in msgs]
    # print(msgs)
    # qr = llm.query(
    #     messages=msgs,
    #     tools=[campaign_tool.to_tool_list()[0].metadata.to_openai_tool()],
    #     tool_choice="auto",
    #     validate=True,
    #     # required_fields=["steps"],
    # )
    # print(qr.response)

    # r = agent.chat("Make a campaign ")
    # pprint(r)
    # r = agent.chat("Sure, send them emails")
    # pprint(r)
    # r = agent.chat("Umm, to the head of google")
    # pprint(r)
