from sqlalchemy.orm import Session

from app.database.models import AgentMessage


class ConversationMemory:
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
    def get(self, db: Session, session_id: str) -> list[dict[str, str]]:
        messages = (
            db.query(AgentMessage)
            .filter(AgentMessage.session_id == session_id)
            .order_by(AgentMessage.created_at.desc(), AgentMessage.id.desc())
            .limit(self.max_messages)
            .all()
        )
        return [
            {"role": message.role, "content": message.content}
            for message in reversed(messages)
        ]

    def add(self, db: Session, session_id: str, role: str, content: str) -> None:
        db.add(AgentMessage(session_id=session_id, role=role, content=content))
        db.commit()

    def clear(self, db: Session, session_id: str) -> None:
        db.query(AgentMessage).filter(AgentMessage.session_id == session_id).delete()
        db.commit()


conversation_memory = ConversationMemory()
