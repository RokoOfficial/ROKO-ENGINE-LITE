#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wrapper SQLite (WAL) para o HGR."""
from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from typing import Any, List, Optional

logger = logging.getLogger(__name__)


class HGRDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()
        self._migrate_v5()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS chat_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    session_id TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_chat_user_ts
                    ON chat_log(user_id, timestamp DESC);

                CREATE TABLE IF NOT EXISTS facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    importance REAL DEFAULT 0.5,
                    category TEXT DEFAULT 'general',
                    tags TEXT DEFAULT '[]',
                    access_count INTEGER DEFAULT 0,
                    last_accessed REAL,
                    created_at REAL NOT NULL,
                    UNIQUE(user_id, key)
                );

                CREATE TABLE IF NOT EXISTS context_steps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    session_id TEXT,
                    query TEXT,
                    thought TEXT,
                    action TEXT,
                    confidence REAL DEFAULT 0.5,
                    importance REAL DEFAULT 0.5,
                    tool_used TEXT,
                    tool_result TEXT,
                    keywords TEXT,
                    timestamp REAL NOT NULL,
                    status TEXT DEFAULT 'success',
                    parallel_group TEXT DEFAULT '',
                    tool_args TEXT DEFAULT '',
                    duration_ms INTEGER
                );
                CREATE INDEX IF NOT EXISTS idx_steps_user_ts
                    ON context_steps(user_id, timestamp DESC);

                CREATE TABLE IF NOT EXISTS cron_jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    schedule TEXT NOT NULL,
                    task_type TEXT DEFAULT 'agent',
                    task TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    last_run REAL,
                    next_run REAL,
                    run_count INTEGER DEFAULT 0,
                    last_output TEXT,
                    created_at REAL NOT NULL
                );
                """
            )

    def _migrate_v5(self) -> None:
        """Adiciona colunas v5 em context_steps se ainda não existirem (não destrutivo)."""
        with self._connect() as conn:
            cols = {r["name"] for r in conn.execute("PRAGMA table_info(context_steps)").fetchall()}
            alterations = []
            if "status" not in cols:
                alterations.append(
                    "ALTER TABLE context_steps ADD COLUMN status TEXT DEFAULT 'success'"
                )
            if "parallel_group" not in cols:
                alterations.append(
                    "ALTER TABLE context_steps ADD COLUMN parallel_group TEXT DEFAULT ''"
                )
            if "tool_args" not in cols:
                alterations.append(
                    "ALTER TABLE context_steps ADD COLUMN tool_args TEXT DEFAULT ''"
                )
            if "duration_ms" not in cols:
                alterations.append(
                    "ALTER TABLE context_steps ADD COLUMN duration_ms INTEGER"
                )
            for sql in alterations:
                conn.execute(sql)
            if alterations:
                conn.commit()
                logger.info("HGR v5 migration: %s coluna(s) em context_steps", len(alterations))

    def execute(self, sql: str, params: tuple = ()) -> int:
        with self._connect() as conn:
            cur = conn.execute(sql, params)
            conn.commit()
            return cur.lastrowid or cur.rowcount

    def fetchone(self, sql: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        with self._connect() as conn:
            return conn.execute(sql, params).fetchone()

    def fetchall(self, sql: str, params: tuple = ()) -> List[sqlite3.Row]:
        with self._connect() as conn:
            return list(conn.execute(sql, params).fetchall())
