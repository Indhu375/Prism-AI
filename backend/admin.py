from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel

from middleware import get_admin_user
import database
import aiosqlite

router = APIRouter(prefix="/admin", tags=["Admin"])

class UserUpdateRequest(BaseModel):
    tier: str
    role: str
    is_active: bool

class UserAdminResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    tier: str
    is_active: bool
    created_at: str
    last_login: str | None

class AdminStatsResponse(BaseModel):
    total_users: int
    total_blogs: int
    total_videos: int
    total_images: int

@router.get("/users", response_model=List[UserAdminResponse])
async def list_users(admin_user: dict = Depends(get_admin_user)):
    """List all registered users. Admin only."""
    async with aiosqlite.connect(database.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users ORDER BY created_at DESC") as cursor:
            rows = await cursor.fetchall()
            users = []
            for row in rows:
                user_dict = dict(row)
                user_dict['is_active'] = bool(user_dict['is_active'])
                users.append(user_dict)
            return users

@router.get("/stats", response_model=AdminStatsResponse)
async def get_stats(admin_user: dict = Depends(get_admin_user)):
    """Get platform-wide generation stats. Admin only."""
    async with aiosqlite.connect(database.DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as c:
            users_count = (await c.fetchone())[0]
            
        async with db.execute("SELECT COUNT(*) FROM usage_logs WHERE endpoint = 'generate-blog'") as c:
            blogs_count = (await c.fetchone())[0]
            
        async with db.execute("SELECT COUNT(*) FROM usage_logs WHERE endpoint = 'generate-video-script'") as c:
            videos_count = (await c.fetchone())[0]
            
        async with db.execute("SELECT COUNT(*) FROM usage_logs WHERE endpoint = 'generate-image'") as c:
            images_count = (await c.fetchone())[0]
            
        return AdminStatsResponse(
            total_users=users_count,
            total_blogs=blogs_count,
            total_videos=videos_count,
            total_images=images_count
        )

@router.put("/users/{user_id}")
async def update_user(user_id: str, request: UserUpdateRequest, admin_user: dict = Depends(get_admin_user)):
    """Update a user's subscription tier, role, and active status. Admin only."""
    if request.tier not in ["free", "pro", "business"]:
        raise HTTPException(status_code=400, detail="Invalid tier")
    if request.role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
        
    async with aiosqlite.connect(database.DB_PATH) as db:
        await db.execute(
            "UPDATE users SET tier = ?, role = ?, is_active = ? WHERE id = ?", 
            (request.tier, request.role, int(request.is_active), user_id)
        )
        await db.commit()
        
    return {"message": "User updated successfully"}
