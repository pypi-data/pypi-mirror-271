from pi_conf import Config, load_config
cfg = load_config("qai")
cfg.to_env()

from llama_index.agent.openai import OpenAIAssistantAgent

agent = OpenAIAssistantAgent.from_new(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    openai_tools=[{"type": "code_interpreter"}],
    instructions_prefix="Please address the user as Jane Doe. The user has a premium account.",
)