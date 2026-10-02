#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gestão de factos persistentes (chave-valor por utilizador)."""
from __future__ import annotations

import json
import re
import time
from typing import Any, Dict, List, Optional

from .database import HGRDatabase


_EXTRACT_PATTERNS = [
    (re.compile(r"(?:me chamo|meu nome é|my name is)\s+([A-Za-zÀ-ÿ]{2,40})", re.I), "nome", 0.95),
    (re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"), "email", 0.90),
    (re.compile(r"(?:sou de|moro em|vivo em|I live in|I'm from)\s+([A-Za-zÀ-ÿ\s]{2,40})", re.I), "localizacao", 0.70),
    (re.compile(r"(?:projeto|project)\s+(?:ativo|atual|current)?\s*[:=]?\s*([A-Za-z0-9_\-.]{2,40})", re.I), "projeto_ativo", 0.75),
    (re.compile(r"(?:prefiro|trabalho com|I prefer|I use)\s+(Python|JavaScript|TypeScript|Go|Rust|Java|C\+\+)", re.I), "linguagem_preferida", 0.80),
]


class FactsManager:
    def __init__(self, db: HGRDatabase, max_in_prompt: int = 20):
        self.db = db
        self.max_in_prompt = max_in_prompt

    def store(
        self,
        user_id: str,
        key: str,
        value: str,
        importance: float = 0.5,
        category: str = "general",
        tags: Optional[List[str]] = None,
    ) -> bool:
        now = time.time()
        tags_json = json.dumps(tags or [])
        existing = self.db.fetchone(
            "SELECT id FROM facts WHERE user_id=? AND key=?", (user_id, key)
        )
        if existing:
            self.db.execute(
                """UPDATE facts SET value=?, importance=?, category=?, tags=?,
                   last_accessed=? WHERE user_id=? AND key=?""",
                (str(value), float(importance), category, tags_json, now, user_id, key),
            )
            return False
        self.db.execute(
            """INSERT INTO facts (user_id, key, value, importance, category, tags, created_at, last_accessed)
               VALUES (?,?,?,?,?,?,?,?)""",
            (user_id, key, str(value), float(importance), category, tags_json, now, now),
        )
        return True

    def get(self, user_id: str, key: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone(
            "SELECT * FROM facts WHERE user_id=? AND key=?", (user_id, key)
        )
        if not row:
            return None
        self.db.execute(
            "UPDATE facts SET access_count=access_count+1, last_accessed=? WHERE id=?",
            (time.time(), row["id"]),
        )
        return dict(row)

    def get_all(self, user_id: str, min_importance: float = 0.0) -> Dict[str, Dict[str, Any]]:
        rows = self.db.fetchall(
            "SELECT * FROM facts WHERE user_id=? AND importance>=? ORDER BY importance DESC",
            (user_id, min_importance),
        )
        return {r["key"]: dict(r) for r in rows}

    def search(self, user_id: str, term: str) -> List[Dict[str, Any]]:
        term = f"%{(term or '').lower()}%"
        rows = self.db.fetchall(
            """SELECT * FROM facts WHERE user_id=? AND
               (LOWER(key) LIKE ? OR LOWER(value) LIKE ? OR LOWER(category) LIKE ?)
               ORDER BY importance DESC""",
            (user_id, term, term, term),
        )
        return [dict(r) for r in rows]

    def delete(
        self,
        user_id: str,
        key: Optional[str] = None,
        category: Optional[str] = None,
        fact_id: Optional[int] = None,
        delete_all: bool = False,
    ) -> int:
        if delete_all:
            return self.db.execute("DELETE FROM facts WHERE user_id=?", (user_id,))
        if fact_id is not None:
            return self.db.execute(
                "DELETE FROM facts WHERE user_id=? AND id=?", (user_id, fact_id)
            )
        if key:
            return self.db.execute(
                "DELETE FROM facts WHERE user_id=? AND key=?", (user_id, key)
            )
        if category:
            return self.db.execute(
                "DELETE FROM facts WHERE user_id=? AND category=?", (user_id, category)
            )
        return 0

    def extract_from_text(self, user_id: str, text: str) -> List[str]:
        found: List[str] = []
        for pattern, category, importance in _EXTRACT_PATTERNS:
            m = pattern.search(text or "")
            if m:
                value = m.group(1).strip()
                key = category
                self.store(user_id, key, value, importance=importance, category="auto_extracted")
                found.append(key)
        return found

    def format_for_prompt(self, user_id: str) -> str:
        facts = list(self.get_all(user_id).values())[: self.max_in_prompt]
        if not facts:
            return ""
        lines = [f"- {f['key']}: {f['value']}" for f in facts]
        return "Known facts about the user:\n" + "\n".join(lines)

    def stats(self, user_id: str) -> Dict[str, Any]:
        rows = self.db.fetchall(
            "SELECT category, COUNT(*) as c FROM facts WHERE user_id=? GROUP BY category",
            (user_id,),
        )
        total = self.db.fetchone(
            "SELECT COUNT(*) as c FROM facts WHERE user_id=?", (user_id,)
        )
        return {
            "total": total["c"] if total else 0,
            "by_category": {r["category"]: r["c"] for r in rows},
        }
