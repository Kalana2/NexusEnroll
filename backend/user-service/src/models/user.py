from enum import Enum
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional

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
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    role: Optional[UserRole] = UserRole.STUDENT
    
    @validator('username')
    def username_must_be_valid(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        return v.lower()
    
    @validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
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
