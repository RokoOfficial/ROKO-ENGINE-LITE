#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scheduler de jobs (cron / every:Ns/Nm/Nh)."""
from __future__ import annotations

import re
import time
from typing import Any, Callable, Dict, List, Optional

from .database import HGRDatabase


def _parse_next_run(schedule: str, from_ts: Optional[float] = None) -> float:
    """Calcula próximo run a partir de now (ou from_ts)."""
    now = from_ts or time.time()
    schedule = (schedule or "").strip().lower()
    m = re.match(r"every:(\d+)(s|m|h)", schedule)
    if m:
        n, unit = int(m.group(1)), m.group(2)
        delta = n if unit == "s" else n * 60 if unit == "m" else n * 3600
        return now + delta
    # cron simples: "M H * * *" (minuto hora) — aproximação: próxima ocorrência no dia
    parts = schedule.split()
    if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
        minute, hour = int(parts[0]), int(parts[1])
        import datetime as dt

        t = dt.datetime.utcfromtimestamp(now)
        target = t.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target.timestamp() <= now:
            target = target + dt.timedelta(days=1)
        return target.timestamp()
    return now + 3600  # default 1h


class CronManager:
    def __init__(self, db: HGRDatabase):
        self.db = db
        self._executor: Optional[Callable] = None

    def set_executor(self, fn: Callable) -> None:
        self._executor = fn

    def create(
        self,
        user_id: str,
        name: str,
        schedule: str,
        task: str,
        description: str = "",
        task_type: str = "agent",
    ) -> Dict[str, Any]:
        now = time.time()
        next_run = _parse_next_run(schedule, now)
        job_id = self.db.execute(
            """INSERT INTO cron_jobs
               (user_id, name, description, schedule, task_type, task, status,
                next_run, created_at)
               VALUES (?,?,?,?,?,?, 'active', ?,?)""",
            (user_id, name, description, schedule, task_type, task, next_run, now),
        )
        return self.get(job_id, user_id) or {"id": job_id}

    def get(self, job_id: int, user_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone(
            "SELECT * FROM cron_jobs WHERE id=? AND user_id=?", (job_id, user_id)
        )
        return dict(row) if row else None

    def list_jobs(self, user_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        if status:
            rows = self.db.fetchall(
                "SELECT * FROM cron_jobs WHERE user_id=? AND status=? ORDER BY id DESC",
                (user_id, status),
            )
        else:
            rows = self.db.fetchall(
                "SELECT * FROM cron_jobs WHERE user_id=? ORDER BY id DESC", (user_id,)
            )
        return [dict(r) for r in rows]

    def pause(self, job_id: int, user_id: str) -> bool:
        n = self.db.execute(
            "UPDATE cron_jobs SET status='paused' WHERE id=? AND user_id=?",
            (job_id, user_id),
        )
        return n > 0

    def resume(self, job_id: int, user_id: str) -> bool:
        job = self.get(job_id, user_id)
        if not job:
            return False
        next_run = _parse_next_run(job["schedule"])
        self.db.execute(
            "UPDATE cron_jobs SET status='active', next_run=? WHERE id=? AND user_id=?",
            (next_run, job_id, user_id),
        )
        return True

    def delete(self, job_id: int, user_id: str) -> bool:
        n = self.db.execute(
            "DELETE FROM cron_jobs WHERE id=? AND user_id=?", (job_id, user_id)
        )
        return n > 0

    def run_now(self, job_id: int, user_id: str) -> Dict[str, Any]:
        job = self.get(job_id, user_id)
        if not job:
            return {"ok": False, "error": "job not found"}
        output = f"[simulated] executed task: {job['task']}"
        if self._executor:
            try:
                output = str(self._executor(job))
            except Exception as e:
                output = f"error: {e}"
        now = time.time()
        next_run = _parse_next_run(job["schedule"], now)
        self.db.execute(
            """UPDATE cron_jobs SET last_run=?, next_run=?, run_count=run_count+1,
               last_output=? WHERE id=?""",
            (now, next_run, output[:2000], job_id),
        )
        return {"ok": True, "job_id": job_id, "output": output, "next_run": next_run}

    def format_next_run(self, job: Dict[str, Any]) -> str:
        nr = job.get("next_run")
        if not nr:
            return "n/a"
        delta = max(0, nr - time.time())
        if delta < 60:
            return f"em {int(delta)}s"
        if delta < 3600:
            return f"em {int(delta // 60)}min"
        return f"em {delta / 3600:.1f}h"
