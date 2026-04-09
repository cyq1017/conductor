"""Memory System — persistent cross-session knowledge store.

A lightweight, file-based memory system that stores facts, decisions,
and lessons learned across sessions. No external dependencies needed.

Storage: JSON file at docs/memory.json
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


# Memory entry types
MEMORY_TYPES = ["fact", "decision", "lesson", "preference", "context"]


@dataclass
class MemoryEntry:
    """A single memory entry."""

    id: int
    type: str  # fact, decision, lesson, preference, context
    content: str
    tags: list[str] = field(default_factory=list)
    source: str = ""  # Where this memory came from
    created: str = ""
    last_accessed: str = ""
    access_count: int = 0

    def matches(self, query: str) -> bool:
        """Check if this entry matches a search query (case-insensitive)."""
        query_lower = query.lower()
        # Check content
        if query_lower in self.content.lower():
            return True
        # Check tags
        if any(query_lower in tag.lower() for tag in self.tags):
            return True
        # Check type
        if query_lower == self.type:
            return True
        return False


@dataclass
class MemoryStore:
    """The memory store for a project."""

    project_name: str
    entries: list[MemoryEntry] = field(default_factory=list)
    next_id: int = 1

    def add(
        self,
        content: str,
        memory_type: str = "fact",
        tags: Optional[list[str]] = None,
        source: str = "",
    ) -> MemoryEntry:
        """Add a new memory entry."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = MemoryEntry(
            id=self.next_id,
            type=memory_type,
            content=content,
            tags=tags or [],
            source=source,
            created=now,
            last_accessed=now,
            access_count=0,
        )
        self.entries.append(entry)
        self.next_id += 1
        return entry

    def search(self, query: str) -> list[MemoryEntry]:
        """Search memories by content, tags, or type."""
        results = []
        for entry in self.entries:
            if entry.matches(query):
                entry.access_count += 1
                entry.last_accessed = datetime.now().strftime("%Y-%m-%d %H:%M")
                results.append(entry)
        return results

    def get_by_type(self, memory_type: str) -> list[MemoryEntry]:
        """Get all memories of a specific type."""
        return [e for e in self.entries if e.type == memory_type]

    def get_recent(self, n: int = 10) -> list[MemoryEntry]:
        """Get the N most recently created memories."""
        sorted_entries = sorted(
            self.entries, key=lambda e: e.created, reverse=True
        )
        return sorted_entries[:n]

    def get_frequent(self, n: int = 10) -> list[MemoryEntry]:
        """Get the N most frequently accessed memories."""
        sorted_entries = sorted(
            self.entries, key=lambda e: e.access_count, reverse=True
        )
        return sorted_entries[:n]

    def delete(self, memory_id: int) -> bool:
        """Delete a memory by ID."""
        for i, entry in enumerate(self.entries):
            if entry.id == memory_id:
                self.entries.pop(i)
                return True
        return False

    def stats(self) -> dict:
        """Get memory store statistics."""
        type_counts = {}
        for entry in self.entries:
            type_counts[entry.type] = type_counts.get(entry.type, 0) + 1
        return {
            "total": len(self.entries),
            "by_type": type_counts,
            "total_tags": len(set(
                tag for entry in self.entries for tag in entry.tags
            )),
        }


def load_memory(project_path: Path) -> MemoryStore:
    """Load memory store from disk."""
    memory_file = project_path / "docs" / "memory.json"

    if not memory_file.exists():
        return MemoryStore(project_name=project_path.name)

    try:
        data = json.loads(memory_file.read_text(encoding="utf-8"))
        store = MemoryStore(
            project_name=data.get("project_name", project_path.name),
            next_id=data.get("next_id", 1),
        )
        for entry_data in data.get("entries", []):
            store.entries.append(MemoryEntry(**entry_data))
        return store
    except (json.JSONDecodeError, KeyError, TypeError):
        return MemoryStore(project_name=project_path.name)


def save_memory(store: MemoryStore, project_path: Path) -> None:
    """Save memory store to disk."""
    memory_file = project_path / "docs" / "memory.json"
    memory_file.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "project_name": store.project_name,
        "next_id": store.next_id,
        "entries": [asdict(e) for e in store.entries],
    }

    memory_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def export_memory_markdown(store: MemoryStore) -> str:
    """Export memory store as readable markdown.

    This can be included in agent prompts for context injection.
    """
    lines = [
        f"# Project Memory: {store.project_name}\n",
        f"> {len(store.entries)} memories stored\n\n",
    ]

    for memory_type in MEMORY_TYPES:
        entries = store.get_by_type(memory_type)
        if not entries:
            continue

        type_labels = {
            "fact": "📌 Facts",
            "decision": "📋 Decisions",
            "lesson": "📖 Lessons Learned",
            "preference": "⚙️ Preferences",
            "context": "🔍 Context",
        }

        lines.append(f"## {type_labels.get(memory_type, memory_type)}\n\n")
        for entry in entries:
            tags_str = " ".join(f"`#{tag}`" for tag in entry.tags) if entry.tags else ""
            lines.append(f"- {entry.content} {tags_str}\n")
        lines.append("\n")

    return "".join(lines)


def auto_extract_memories(project_path: Path) -> list[MemoryEntry]:
    """Automatically extract potential memories from HANDOFF.md.

    Returns new entries that haven't been stored yet.
    """
    store = load_memory(project_path)
    existing_contents = {e.content.lower() for e in store.entries}
    new_entries = []

    handoff = project_path / "HANDOFF.md"
    if not handoff.exists():
        return new_entries

    try:
        content = handoff.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return new_entries

    # Extract decisions as potential memories
    decision_patterns = [
        (r"-\s*decisions?\s*:\s*(.+)", "decision"),
        (r"-\s*chose\s+(.+)", "decision"),
        (r"-\s*selected\s+(.+)", "decision"),
    ]

    for pattern, mem_type in decision_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            text = match.group(1).strip()
            if text.lower() not in existing_contents and len(text) > 10:
                entry = store.add(text, mem_type, source="HANDOFF.md (auto)")
                new_entries.append(entry)
                existing_contents.add(text.lower())

    # Extract pitfalls as lessons
    pitfall_patterns = [
        (r"-\s*pitfalls?\s*:\s*(.+)", "lesson"),
    ]

    for pattern, mem_type in pitfall_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            text = match.group(1).strip()
            if text.lower() not in existing_contents and len(text) > 10:
                entry = store.add(text, mem_type, source="HANDOFF.md (auto)")
                new_entries.append(entry)
                existing_contents.add(text.lower())

    if new_entries:
        save_memory(store, project_path)

    return new_entries
