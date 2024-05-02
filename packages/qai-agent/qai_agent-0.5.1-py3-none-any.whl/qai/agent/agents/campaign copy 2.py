import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, List, Optional, Self, Sequence, Type, TypeVar

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
from pi_conf import AttrDict, load_config
from pi_log import logs
from pydantic import BaseModel, Field
from qai.ai import MessageRole, QueryReturn, to_message
from qai.ai.frameworks.openai.llm import OpenAILLM
from sqlalchemy import create_engine

from qai.agent.agents.find_agent import AgentType, FindAgentWorker
from qai.agent.qaibot import QaiSession
from qai.agent.sessions.qai_session import QaiSession
from qai.agent.tools.types import StringEnum

class OutreachType(StringEnum):
    email = "email"
    linkedin = "linkedin"
    phone = "phone"
    whatsapp = "whatsapp"


class CompanyCampaignModel(BaseModel):
    people: list[str] = Field(description="A list of people to generate a campaign for.")
    companies: list[str] = Field(description="A list of companies to generate a campaign for.")
    outreach_types: list[OutreachType] = Field(
        description="The type of outreach to use for the campaign."
    )


def create_campaign(
    people: list[str],
    companies: list[str],
    outreach_types: list[str],
) -> str:
    print(
        f"Creating campaign for people: {people} companies: {companies}"
        f" outreach_types: {outreach_types}"
    )

    return "Campaign created"


class CreateCampaign(OpenAIAgent):
    """An Agent to create a campaign for a list of people and companies."""

    name: str = "create_campaign"
    description: str = (
        f"Create a campaign for a list of people and companies. "
        f"Only use following outreach types: [{','.join([str(e) for e in OutreachType])}]"
    )

    @classmethod
    def create(
        cls,
        nametools: Sequence[BaseTool] = None,
        llm: LLM = None,
        *args,
        **kwargs: Any,
    ):
        create_campaign_tool = FunctionTool.from_defaults(
            name=cls.name,
            fn=create_campaign,
            tool_metadata=ToolMetadata(
                name=cls.name,
                description=cls.description,
                fn_schema=CompanyCampaignModel,
            ),
        )
        agent = CreateCampaign.from_tools(
            llm=llm,
            tools=[create_campaign_tool],
        )
        
        return agent
