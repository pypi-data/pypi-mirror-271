import os
from abc import abstractmethod
from collections import deque
from typing import Any, Deque, Dict, List, Optional, Tuple, Union, cast

import llama_index.core.instrumentation as instrument
from llama_index.agent.openai import OpenAIAgent
from llama_index.core import ChatPromptTemplate, PromptTemplate
from llama_index.core.agent import AgentChatResponse, CustomSimpleAgentWorker, Task
from llama_index.core.agent.runner.base import AgentRunner, dispatcher
from llama_index.core.agent.types import (
    BaseAgent,
    BaseAgentWorker,
    Task,
    TaskStep,
    TaskStepOutput,
)
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.bridge.pydantic import BaseModel, Field, PrivateAttr
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
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.llms.llm import LLM
from llama_index.core.memory import BaseMemory, ChatMemoryBuffer
from llama_index.core.memory.types import BaseMemory
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import PydanticSingleSelector
from llama_index.core.tools import BaseTool, QueryEngineTool
from llama_index.core.tools.types import BaseTool

from qai.agent import ROOT_DIR, cfg
from qai.agent.agents.find_agent import AgentType, FindAgentWorker
from qai.agent.agents.sql_query import RefineSQLQuery
from qai.agent.models import OutreachType
from qai.agent.qaibot import QaiBot, QaiSession
from qai.agent.sessions.qai_session import QaiSession
from qai.agent.tools.types import StringEnum


class ResponseEval(BaseModel):
    """Evaluation of whether the response has an error."""

    has_error: bool = Field(..., description="Whether the response has an error.")
    new_question: str = Field(..., description="The suggested new question.")
    explanation: str = Field(
        ...,
        description=(
            "The explanation for the error as well as for the new question."
            "Can include the direct stack trace as well."
        ),
    )


class CampaignAgent(OpenAIAgent):

    people_ids: Optional[list[str]] = Field(
        description="A list of people to generate a campaign for."
    )
    company_ids: Optional[list[str]] = Field(
        description="A list of companies to generate a campaign for."
    )
    outreach_types: Optional[list[OutreachType]] = Field(
        description="The type of outreach to use for the campaign."
    )
    def __init__(self, tools: List[BaseTool], **kwargs: Any) -> None:
        """Init params."""
        super().__init__(
            tools=tools,
            **kwargs,
        )

    def _initialize_state(self, task: Task, **kwargs: Any) -> Dict[str, Any]:
        """Initialize state."""
        print(f"Initializing state for task {task} with kwargs {kwargs}")
        return {"count": 0, "current_reasoning": []}

    def _run_step(
        self,
        task_id: str,
        step: Optional[TaskStep] = None,
        input: Optional[str] = None,
        mode: ChatResponseMode = ChatResponseMode.WAIT,
        **kwargs: Any,
    ) -> TaskStepOutput:
        print(f"_run_step:    Task {task_id}: Step {step} with input={input}, mode={mode} and kwargs {kwargs}")
        step_output = super()._run_step(task_id, step, input, mode, **kwargs)
        user_input = step_output.task_step.input
        print(f"  ~_run_step: user_input={user_input}")
        
        # refine_tools = RefineSQLQuery(
        #     uri=cfg.db.uri,
        # )

        # refining_agent = OpenAIAgent.from_tools(refine_tools.to_tool_list(), verbose=True)
        # r = refining_agent.chat(input, tool_choice="find_steps")
        # refined_query = refine_tools.get_return_query(r)

        # print(f" ###### Q2 = {refined_query} ######")
        # r2 = refining_agent.chat(refined_query)

        # step_output.
        print(f"  ~_run_step: task_steps={step_output.task_step} next_steps={step_output.next_steps} {step_output}")
        return step_output

    def _finalize_task(self, task: Task, **kwargs: Any) -> None:
        """Finalize task."""
        print(f"Finalizing task with state {task} and kwargs {kwargs}")
        # nothing to finalize here
        # this is usually if you want to modify any sort of
        # internal state beyond what is set in `_initialize_state`
