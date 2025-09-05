from enum import Enum
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional, Tuple, Any, Callable
from supabase import Client, create_client
import hashlib


SUPABASE_URL = "https://gcepytafvxmgddfrhpah.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZXB5dGFmdnhtZ2RkZnJocGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNjA2NTAsImV4cCI6MjA3MjYzNjY1MH0.vE3i9vOh2ZItBE4zp7FcCvoEOmtCdU4_MkUZSB4MhTo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class UserState(str, Enum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    PENDING = "Pending"


class UserRole(str, Enum):
    STUDENT = "Student"
    FACULTY = "Faculty"
    ADMIN = "Admin"


class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    state: UserState
    created_at: datetime
    updated_at: datetime

    class Config:
        use_enum_values = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    role: Optional[UserRole] = UserRole.STUDENT

    @validator("username")
    def username_must_be_valid(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v.lower()

    @validator("password")
    def password_must_be_strong(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    state: Optional[UserState] = None


class UserStateUpdate(BaseModel):
    state: UserState


class UserRoleUpdate(BaseModel):
    role: UserRole


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    success: bool
    user: User
    message: Optional[str] = None


class UsersResponse(BaseModel):
    success: bool
    users: list[User]
    count: int


class LoginResponse(BaseModel):
    success: bool
    token: str
    user: User
    expires_at: str


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_user_by_id(user_id: str) -> Optional[User]:
    resp = supabase.table("users").select("*").eq("id", user_id).execute()
    data = resp.data or []
    if not data:
        return None
    return User.parse_obj(data[0])


def get_users(limit: int = 100, offset: int = 0) -> Tuple[list[User], int]:
    start = offset
    end = offset + max(0, limit - 1)
    resp = supabase.table("users").select("*").range(start, end).execute()
    data = resp.data or []
    users = [User.parse_obj(u) for u in data]
    return users, len(users)


def create_user(user_create: UserCreate) -> User:
    payload = user_create.dict()
    password = payload.pop("password")
    payload["password_hash"] = _hash_password(password)
    # ensure role stored as string
    if isinstance(payload.get("role"), UserRole):
        payload["role"] = payload["role"].value
    payload["state"] = UserState.PENDING.value
    payload["created_at"] = datetime.utcnow().isoformat()
    payload["updated_at"] = payload["created_at"]
    resp = supabase.table("users").insert(payload).execute()
    data = resp.data or []
    return User.parse_obj(data[0])


def update_user(user_id: str, user_update: UserUpdate) -> Optional[User]:
    payload = user_update.dict(exclude_none=True)
    if "password" in payload:
        payload["password_hash"] = _hash_password(payload.pop("password"))
    if "role" in payload and isinstance(payload["role"], UserRole):
        payload["role"] = payload["role"].value
    if "state" in payload and isinstance(payload["state"], UserState):
        payload["state"] = payload["state"].value
    payload["updated_at"] = datetime.utcnow().isoformat()
    # build the request and call select dynamically to satisfy static type checkers;
    # build the request and call select dynamically to satisfy static type checkers;
    # if select is not available, fall back to executing the update directly
    req = supabase.table("users").update(payload).eq("id", user_id)
    select_fn: Optional[Callable[..., Any]] = getattr(req, "select", None)
    if callable(select_fn):
        resp = select_fn("*").execute()
    else:
        resp = req.execute()
    data = resp.data or []
    if not data:
        return None
    return User.parse_obj(data[0])


def delete_user(user_id: str) -> bool:
    resp = supabase.table("users").delete().eq("id", user_id).execute()
    # APIResponse may not expose 'error' as a static attribute in type hints; use getattr for safety
    return getattr(resp, "error", None) is None


def authenticate_user(username: str, password: str) -> Optional[User]:
    resp = (
        supabase.table("users").select("*").eq("username", username.lower()).execute()
    )
    data = resp.data or []
    if not data:
        return None
    record = data[0]
    stored = record.get("password_hash") or record.get("password")
    if stored and stored == _hash_password(password):
        return User.parse_obj(record)
    return None
