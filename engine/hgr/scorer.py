#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scoring de relevância por keywords (Jaccard + recência)."""
from __future__ import annotations

import re
import time
from typing import Set


_STOP = {
    "o", "a", "os", "as", "de", "da", "do", "das", "dos", "em", "no", "na",
    "para", "com", "por", "um", "uma", "e", "ou", "que", "se", "ao", "à",
    "the", "is", "and", "or", "to", "in", "of", "for", "on", "at", "a", "an",
}


class RelevanceScorer:
    @staticmethod
    def keywords(text: str) -> Set[str]:
        words = re.findall(r"\b\w+\b", (text or "").lower())
        return {w for w in words if len(w) > 2 and w not in _STOP}

    @staticmethod
    def score(query: str, text: str, timestamp: float = 0.0, access_count: int = 0) -> float:
        qk = RelevanceScorer.keywords(query)
        tk = RelevanceScorer.keywords(text)
        if not qk or not tk:
            return 0.0
        inter = len(qk & tk)
        union = len(qk | tk)
        jaccard = inter / union if union else 0.0
        age_days = max(0.0, (time.time() - timestamp) / 86400.0) if timestamp else 0.0
        decay = max(0.3, 1.0 - age_days * 0.05)
        boost = min(0.2, access_count * 0.02)
        return min(1.0, jaccard * decay + boost)

    @staticmethod
    def importance(
        thought: str,
        confidence: float = 0.5,
        has_result: bool = False,
        status: str = "success",
        error_floor: float = 0.45,
    ) -> float:
        """
        Calcula importância de um step.
        v5: status error/timeout eleva o floor para falhas úteis persistirem.
        """
        base = float(confidence or 0.5)
        important = {
            "error", "critical", "important", "bug", "fix", "solution",
            "erro", "importante", "timeout", "falha", "failed",
        }
        text = (thought or "").lower()
        boost = sum(0.08 for w in important if w in text)
        if has_result:
            boost += 0.1
        score = min(1.0, base + boost)
        st = (status or "success").lower()
        if st in ("error", "timeout", "failed"):
            score = max(score, error_floor + (0.1 if has_result else 0.0))
        return min(1.0, score)
