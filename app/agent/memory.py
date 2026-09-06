from threading import Lock


class ConversationMemory:
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self._conversations: dict[str, list[dict[str, str]]] = {}
        self._lock = Lock()

    def get(self, session_id: str) -> list[dict[str, str]]:
        with self._lock:
            return list(self._conversations.get(session_id, []))

    def add(self, session_id: str, role: str, content: str) -> None:
        with self._lock:
            messages = self._conversations.setdefault(session_id, [])
            messages.append({"role": role, "content": content})
            self._conversations[session_id] = messages[-self.max_messages:]

    def clear(self, session_id: str) -> None:
        with self._lock:
            self._conversations.pop(session_id, None)


conversation_memory = ConversationMemory()
