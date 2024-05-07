from __future__ import annotations

from pydantic import BaseModel


class Repo(BaseModel):
    uuid: str
    name: str
    description: str | None
