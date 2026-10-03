"""
CareerLens AI - Authentication Pattern Example

Public portfolio sample demonstrating the authentication architecture.
The complete implementation is maintained in the private repository.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt


@dataclass
class TokenPayload:
    user_id: int
    role: str


class TokenService:
    """Example JWT access-token service."""

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_minutes: int = 30,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_minutes = access_token_minutes

    def create_access_token(self, user_id: int, role: str) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "role": role,
            "iat": now,
            "exp": now + timedelta(minutes=self.access_token_minutes),
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode_access_token(self, token: str) -> Optional[TokenPayload]:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            return TokenPayload(
                user_id=int(payload["sub"]),
                role=payload["role"],
            )

        except (jwt.InvalidTokenError, KeyError, ValueError):
            return None


def require_role(user_role: str, required_role: str) -> None:
    """
    Simple RBAC example.

    CareerLens uses authorization checks to protect administrative
    functionality and ownership checks for user-specific resources.
    """

    if user_role != required_role:
        raise PermissionError("Insufficient permissions")