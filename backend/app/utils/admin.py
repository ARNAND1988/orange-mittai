from fastapi import Depends, HTTPException, Request
from app.models.user import User
from app.utils.auth import get_current_user  # wherever this lives

def require_admin(
        request: Request,
        current_user: User = Depends(get_current_user),
):
    # 🚫 Allow CORS preflight to pass through
    if request.method == "OPTIONS":
        return None

    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    print("current user",current_user.email)
    return current_user
