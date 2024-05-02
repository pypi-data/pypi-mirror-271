from enum import StrEnum
from typing import Any, Self, Sequence

from llama_index.agent.openai import OpenAIAgent
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.llms.llm import LLM
from llama_index.core.tools import BaseTool, FunctionTool, QueryEngineTool
from llama_index.core.tools.types import ToolMetadata
from pydantic import BaseModel, Field

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
