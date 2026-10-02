#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Context steps de raciocínio do agente (HGR v5)."""
from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from .database import HGRDatabase
from .scorer import RelevanceScorer


class ContextStepsManager:
    def __init__(
        self,
        db: HGRDatabase,
        importance_threshold: float = 0.3,
        min_relevance: float = 0.05,
        error_importance_floor: float = 0.45,
        persist_error_steps: bool = True,
        max_parallel_in_prompt: int = 8,
    ):
        self.db = db
        self.importance_threshold = importance_threshold
        self.min_relevance = min_relevance
        self.error_importance_floor = error_importance_floor
        self.persist_error_steps = persist_error_steps
        self.max_parallel_in_prompt = max_parallel_in_prompt
        self.scorer = RelevanceScorer()

    def _session_id(self, user_id: str) -> str:
        day = datetime.utcnow().strftime("%Y-%m-%d")
        return hashlib.md5(f"{user_id}:{day}".encode()).hexdigest()[:16]

    def store(self, user_id: str, step: Dict[str, Any]) -> Optional[int]:
        thought = step.get("thought", "")
        confidence = float(step.get("confidence", 0.5))
        has_result = bool(step.get("result") or step.get("tool_result"))
        status = (step.get("status") or "success").lower()
        importance = step.get("importance")
        if importance is None:
            importance = self.scorer.importance(
                thought,
                confidence,
                has_result,
                status=status,
                error_floor=self.error_importance_floor,
            )
        # erros úteis: forçar persistência se configurado
        if (
            self.persist_error_steps
            and status in ("error", "timeout", "failed")
            and float(importance) < self.importance_threshold
        ):
            importance = max(float(importance), self.error_importance_floor)

        if float(importance) < self.importance_threshold and status not in (
            "error",
            "timeout",
            "failed",
            "final",
        ):
            return None

        keywords = " ".join(
            sorted(
                self.scorer.keywords(
                    f"{step.get('query', '')} {thought} {step.get('tool') or step.get('tool_used') or ''}"
                )
            )
        )
        now = time.time()
        tool_args = step.get("tool_args") or step.get("args") or step.get("params") or ""
        if not isinstance(tool_args, str):
            try:
                tool_args = json.dumps(tool_args, ensure_ascii=False, default=str)[:500]
            except Exception:
                tool_args = str(tool_args)[:500]

        return self.db.execute(
            """INSERT INTO context_steps
               (user_id, session_id, query, thought, action, confidence, importance,
                tool_used, tool_result, keywords, timestamp,
                status, parallel_group, tool_args, duration_ms)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                user_id,
                self._session_id(user_id),
                step.get("query", ""),
                thought,
                step.get("action", ""),
                confidence,
                float(importance),
                step.get("tool") or step.get("tool_used"),
                str(step.get("result") or step.get("tool_result") or "")[:300],
                keywords,
                now,
                status,
                step.get("parallel_group") or "",
                tool_args,
                step.get("duration_ms"),
            ),
        )

    def record_steps_batch(
        self,
        user_id: str,
        query: str,
        items: List[Dict[str, Any]],
        parallel_group: str = "",
    ) -> List[Optional[int]]:
        """Grava vários steps do mesmo turno (ex.: tools em paralelo)."""
        ids: List[Optional[int]] = []
        for item in items:
            step = dict(item)
            step.setdefault("query", query)
            if parallel_group:
                step["parallel_group"] = parallel_group
            ids.append(self.store(user_id, step))
        return ids

    def retrieve_relevant(
        self, user_id: str, query: str, max_items: int = 5
    ) -> List[Dict[str, Any]]:
        rows = self.db.fetchall(
            """SELECT * FROM context_steps WHERE user_id=?
               ORDER BY timestamp DESC LIMIT 50""",
            (user_id,),
        )
        scored = []
        for r in rows:
            d = dict(r)
            text = f"{d.get('thought', '')} {d.get('action', '')} {d.get('tool_used', '')} {d.get('tool_result', '')}"
            s = self.scorer.score(query, text, timestamp=float(d.get("timestamp") or 0))
            # boost steps com erro (úteis para não repetir)
            st = (d.get("status") or "success").lower()
            if st in ("error", "timeout", "failed"):
                s = max(s, 0.15)
            if s >= self.min_relevance or st in ("error", "timeout", "failed"):
                scored.append((s, d))
        scored.sort(key=lambda x: (-x[0], -float(x[1].get("timestamp") or 0)))
        return [d for _, d in scored[:max_items]]

    def format_for_prompt(self, user_id: str, query: str, max_items: int = 5) -> str:
        steps = self.retrieve_relevant(user_id, query, max_items=max_items)
        if not steps:
            return ""
        lines = []
        for s in steps:
            st = s.get("status") or "success"
            tool = s.get("tool_used") or ""
            thought = (s.get("thought") or "")[:120]
            result = (s.get("tool_result") or "")[:80]
            pg = s.get("parallel_group") or ""
            extra = f" [{st}]" if st != "success" else ""
            if pg:
                extra += f" group={pg}"
            lines.append(f"- {tool}{extra}: {thought} → {result}".strip())
        return "Recent reasoning steps:\n" + "\n".join(lines)
