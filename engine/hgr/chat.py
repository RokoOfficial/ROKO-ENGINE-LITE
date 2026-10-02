#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Histórico de chat persistente."""
from __future__ import annotations

import hashlib
import time
from datetime import datetime
from typing import Any, Dict, List

from .database import HGRDatabase


class ChatHistoryManager:
    def __init__(self, db: HGRDatabase, max_history: int = 200):
        self.db = db
        self.max_history = max_history

    def _session_id(self, user_id: str) -> str:
        day = datetime.utcnow().strftime("%Y-%m-%d")
        return hashlib.md5(f"{user_id}:{day}".encode()).hexdigest()[:16]

    def add(self, user_id: str, role: str, content: str) -> int:
        now = time.time()
        sid = self._session_id(user_id)
        row_id = self.db.execute(
            """INSERT INTO chat_log (user_id, role, content, timestamp, session_id)
               VALUES (?,?,?,?,?)""",
            (user_id, role, content, now, sid),
        )
        # trim old
        count_row = self.db.fetchone(
            "SELECT COUNT(*) as c FROM chat_log WHERE user_id=?", (user_id,)
        )
        if count_row and count_row["c"] > self.max_history:
            excess = count_row["c"] - self.max_history
            self.db.execute(
                """DELETE FROM chat_log WHERE id IN (
                     SELECT id FROM chat_log WHERE user_id=? ORDER BY timestamp ASC LIMIT ?
                   )""",
                (user_id, excess),
            )
        return row_id

    def get(self, user_id: str, last_n: int = 40) -> List[Dict[str, Any]]:
        rows = self.db.fetchall(
            """SELECT role, content, timestamp, session_id FROM chat_log
               WHERE user_id=? ORDER BY timestamp DESC LIMIT ?""",
            (user_id, last_n),
        )
        return [dict(r) for r in reversed(rows)]

    def clear(self, user_id: str) -> int:
        return self.db.execute("DELETE FROM chat_log WHERE user_id=?", (user_id,))
