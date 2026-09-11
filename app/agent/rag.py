from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class KnowledgeChunk:
    source: str
    text: str
    vector: tuple[float, ...]


_TOKEN_PATTERN = re.compile(r"[a-z0-9_]+", re.IGNORECASE)
_VECTOR_SIZE = 256


def _tokens(text: str) -> list[str]:
    return [token.lower() for token in _TOKEN_PATTERN.findall(text)]


def _embed(text: str) -> tuple[float, ...]:
    vector = [0.0] * _VECTOR_SIZE
    for token in _tokens(text):
        index = hash(token) % _VECTOR_SIZE
        vector[index] += 1.0
    magnitude = math.sqrt(sum(value * value for value in vector))
    return tuple(value / magnitude for value in vector) if magnitude else tuple(vector)


def _similarity(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return sum(a * b for a, b in zip(left, right))


def _chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = max(end - overlap, start + 1)
    return chunks


def load_chunks(directory: Path | None = None) -> list[KnowledgeChunk]:
    knowledge_dir = directory or Path(__file__).parent.parent / "knowledge"
    chunks = []
    for path in knowledge_dir.glob("*.md"):
        for index, text in enumerate(_chunk_text(path.read_text(encoding="utf-8"))):
            chunks.append(KnowledgeChunk(f"{path.name}#{index + 1}", text, _embed(text)))
    return chunks


def retrieve_context(query: str, top_k: int = 3, directory: Path | None = None) -> list[dict[str, str | float]]:
    query_vector = _embed(query)
    ranked = sorted(
        ((_similarity(query_vector, chunk.vector), chunk) for chunk in load_chunks(directory)),
        key=lambda item: item[0],
        reverse=True,
    )
    return [
        {"source": chunk.source, "content": chunk.text, "score": round(score, 4)}
        for score, chunk in ranked[:top_k]
        if score > 0
    ]
