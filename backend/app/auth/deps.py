from fastapi import Depends, HTTPException, status
from typing import Literal

def get_current_role() -> str:
    # Placeholder: Accept role from simple header in real app (or JWT).
    return "clinician"

def require_role(allowed: list[Literal["clinician","admin","researcher"]]):
    def _dep(role: str = Depends(get_current_role)):
        if role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return role
    return _dep
