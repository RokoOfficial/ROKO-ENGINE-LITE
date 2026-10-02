#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auth: registo, login, JWT simples, validação."""
from __future__ import annotations

import hashlib
import hmac
import json
import base64
import re
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from .config import AuthConfig


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


class UserDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    is_admin INTEGER DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS login_attempts (
                    username TEXT,
                    success INTEGER,
                    ts REAL
                );
                CREATE TABLE IF NOT EXISTS revoked_tokens (
                    token_hash TEXT PRIMARY KEY,
                    revoked_at REAL
                );
                """
            )


class AuthManager:
    def __init__(self, config: Optional[AuthConfig] = None):
        self.config = config or AuthConfig()
        self.db = UserDatabase(self.config.db_path)

    def _hash_password(self, password: str) -> str:
        salt = "roko-auth-v1"
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), 100_000
        ).hex()

    def _verify_password(self, password: str, password_hash: str) -> bool:
        return hmac.compare_digest(self._hash_password(password), password_hash)

    def _make_token(self, user: Dict[str, Any]) -> str:
        header = _b64url(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
        exp = int(time.time()) + self.config.jwt_expiration_hours * 3600
        payload = _b64url(
            json.dumps(
                {
                    "sub": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                    "exp": exp,
                }
            ).encode()
        )
        sig_input = f"{header}.{payload}".encode()
        sig = hmac.new(
            self.config.jwt_secret.encode(), sig_input, hashlib.sha256
        ).digest()
        return f"{header}.{payload}.{_b64url(sig)}"

    def _parse_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None
            header_b, payload_b, sig_b = parts
            sig_input = f"{header_b}.{payload_b}".encode()
            expected = hmac.new(
                self.config.jwt_secret.encode(), sig_input, hashlib.sha256
            ).digest()
            if not hmac.compare_digest(_b64url(expected), sig_b):
                return None
            payload = json.loads(_b64url_decode(payload_b))
            if payload.get("exp", 0) < time.time():
                return None
            # revoked?
            th = hashlib.sha256(token.encode()).hexdigest()
            with self.db._connect() as conn:
                row = conn.execute(
                    "SELECT 1 FROM revoked_tokens WHERE token_hash=?", (th,)
                ).fetchone()
                if row:
                    return None
            return payload
        except Exception:
            return None

    def _validate_password(self, password: str) -> Tuple[bool, str]:
        if len(password) < self.config.min_password_length:
            return False, f"password must be at least {self.config.min_password_length} chars"
        return True, "ok"

    def _validate_email(self, email: str) -> Tuple[bool, str]:
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email or ""):
            return False, "invalid email"
        return True, "ok"

    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        username = (username or "").strip()
        email = (email or "").strip().lower()
        if not username or len(username) < 3:
            return {"ok": False, "error": "username too short"}
        ok, msg = self._validate_email(email)
        if not ok:
            return {"ok": False, "error": msg}
        ok, msg = self._validate_password(password)
        if not ok:
            return {"ok": False, "error": msg}
        try:
            with self.db._connect() as conn:
                cur = conn.execute(
                    """INSERT INTO users (username, email, password_hash, created_at)
                       VALUES (?,?,?,?)""",
                    (username, email, self._hash_password(password), time.time()),
                )
                conn.commit()
                user_id = cur.lastrowid
            return {
                "ok": True,
                "user_id": user_id,
                "username": username,
                "message": "registered",
            }
        except sqlite3.IntegrityError:
            return {"ok": False, "error": "username or email already exists"}

    def login(self, username: str, password: str) -> Dict[str, Any]:
        username = (username or "").strip()
        with self.db._connect() as conn:
            # lockout check
            since = time.time() - self.config.lockout_duration_seconds
            fails = conn.execute(
                """SELECT COUNT(*) as c FROM login_attempts
                   WHERE username=? AND success=0 AND ts>?""",
                (username, since),
            ).fetchone()["c"]
            if fails >= self.config.max_login_attempts:
                return {"ok": False, "error": "account temporarily locked"}
            row = conn.execute(
                "SELECT * FROM users WHERE username=? OR email=?",
                (username, username.lower()),
            ).fetchone()
            if not row or not self._verify_password(password, row["password_hash"]):
                conn.execute(
                    "INSERT INTO login_attempts (username, success, ts) VALUES (?,?,?)",
                    (username, 0, time.time()),
                )
                conn.commit()
                return {"ok": False, "error": "invalid credentials"}
            conn.execute(
                "INSERT INTO login_attempts (username, success, ts) VALUES (?,?,?)",
                (username, 1, time.time()),
            )
            conn.commit()
            user = {
                "id": row["id"],
                "username": row["username"],
                "email": row["email"],
            }
            token = self._make_token(user)
            return {"ok": True, "token": token, "user": user}

    def validate_token(self, token: str) -> Dict[str, Any]:
        payload = self._parse_token(token or "")
        if not payload:
            return {"ok": False, "error": "invalid or expired token"}
        return {
            "ok": True,
            "user": {
                "id": payload.get("sub"),
                "username": payload.get("username"),
                "email": payload.get("email"),
            },
        }

    def logout(self, token: str) -> Dict[str, Any]:
        if not token:
            return {"ok": False, "error": "missing token"}
        th = hashlib.sha256(token.encode()).hexdigest()
        with self.db._connect() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO revoked_tokens (token_hash, revoked_at) VALUES (?,?)",
                (th, time.time()),
            )
            conn.commit()
        return {"ok": True}

    def me(self, token: str) -> Dict[str, Any]:
        return self.validate_token(token)
