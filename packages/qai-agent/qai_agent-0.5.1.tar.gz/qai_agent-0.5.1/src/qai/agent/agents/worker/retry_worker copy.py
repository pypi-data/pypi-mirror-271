from typing import Any, Dict, List, Optional, Tuple

from llama_index.agent.openai import OpenAIAgent
from llama_index.core import ChatPromptTemplate, PromptTemplate
from llama_index.core.agent import AgentChatResponse, CustomSimpleAgentWorker, Task
from llama_index.core.bridge.pydantic import BaseModel, Field, PrivateAttr
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import PydanticSingleSelector
from llama_index.core.tools import BaseTool, QueryEngineTool

DEFAULT_PROMPT_STR = """
Given previous question/response pairs, please determine if an error has occurred in the response, and suggest \
    a modified question that will not trigger the error.

Examples of modified questions:
- The question itself is modified to elicit a non-erroneous response
- The question is augmented with context that will help the downstream system better answer the question.
- The question is augmented with examples of negative responses, or other negative questions.

An error means that either an exception has triggered, or the response is completely irrelevant to the question.

Please return the evaluation of the response in the following JSON format.

"""


def get_chat_prompt_template(
    system_prompt: str, current_reasoning: Tuple[str, str]
) -> ChatPromptTemplate:
    system_msg = ChatMessage(role=MessageRole.SYSTEM, content=system_prompt)
    messages = [system_msg]
    for raw_msg in current_reasoning:
        if raw_msg[0] == "user":
            messages.append(ChatMessage(role=MessageRole.USER, content=raw_msg[1]))
        else:
            messages.append(ChatMessage(role=MessageRole.ASSISTANT, content=raw_msg[1]))
    return ChatPromptTemplate(message_templates=messages)


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


class RetryAgentWorker(OpenAIAgent):
    """Agent worker that adds a retry layer on top of a router.

    Continues iterating until there's no errors / task is done.

    """

    prompt_str: str = Field(default=DEFAULT_PROMPT_STR)
    max_iterations: int = Field(default=10)

    _router_query_engine: RouterQueryEngine = PrivateAttr()

    def __init__(self, tools: List[BaseTool], **kwargs: Any) -> None:
        """Init params."""
        # validate that all tools are query engine tools
        for tool in tools:
            if not isinstance(tool, QueryEngineTool):
                raise ValueError(f"Tool {tool.metadata.name} is not a query engine tool.")
        self._router_query_engine = RouterQueryEngine(
            selector=PydanticSingleSelector.from_defaults(),
            query_engine_tools=tools,
            verbose=kwargs.get("verbose", False),
        )
        super().__init__(
            tools=tools,
            **kwargs,
        )

    def _initialize_state(self, task: Task, **kwargs: Any) -> Dict[str, Any]:
        """Initialize state."""
        return {"count": 0, "current_reasoning": []}

    def _run_step(
        self, state: Dict[str, Any], task: Task, input: Optional[str] = None
    ) -> Tuple[AgentChatResponse, bool]:
        """Run step.

        Returns:
            Tuple of (agent_response, is_done)

        """
        if "new_input" not in state:
            new_input = task.input
        else:
            new_input = state["new_input"]

        # first run router query engine
        response = self._router_query_engine.query(new_input)

        # append to current reasoning
        state["current_reasoning"].extend([("user", new_input), ("assistant", str(response))])

        # Then, check for errors
        # dynamically create pydantic program for structured output extraction based on template
        chat_prompt_tmpl = get_chat_prompt_template(self.prompt_str, state["current_reasoning"])
        llm_program = LLMTextCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(output_cls=ResponseEval),
            prompt=chat_prompt_tmpl,
            llm=self.llm,
        )
        # run program, look at the result
        response_eval = llm_program(query_str=new_input, response_str=str(response))
        if not response_eval.has_error:
            is_done = True
        else:
            is_done = False
        state["new_input"] = response_eval.new_question

        if self.verbose:
            print(f"> Question: {new_input}")
            print(f"> Response: {response}")
            print(f"> Response eval: {response_eval.dict()}")

        # return response
        return AgentChatResponse(response=str(response)), is_done

    def _finalize_task(self, state: Dict[str, Any], **kwargs) -> None:
        """Finalize task."""
        # nothing to finalize here
        # this is usually if you want to modify any sort of
        # internal state beyond what is set in `_initialize_state`
        pass
