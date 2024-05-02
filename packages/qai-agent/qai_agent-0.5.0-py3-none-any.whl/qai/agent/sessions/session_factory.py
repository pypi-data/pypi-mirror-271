from qai.agent.qaibot import QaiSession
from qai.agent.tools import Action


def create_session(
    db_config: dict,
    model_config: dict,
    session_id: str = None,
    category: str | Action = None,
    messages: list[dict] = None,
) -> QaiSession:
    if messages is None:
        messages = []
    cls = QaiSession
    if Action.conversation == category:
        from .conversation import ConversationSession

        cls = ConversationSession
    return cls(
        db_config=db_config,
        model_config=model_config,
        session_id=session_id,
        category=category,
        messages=messages,
    )
