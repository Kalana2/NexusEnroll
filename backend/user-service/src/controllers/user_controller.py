from fastapi import APIRouter, HTTPException, Depends, status, Query
from datetime import datetime
from typing import Optional, List
from src.models.user import (
    User, UserCreate, UserUpdate, UserStateUpdate, UserRoleUpdate,
    UserLogin, UserResponse, UsersResponse, LoginResponse, UserState, UserRole
)
from src.services.user_service import UserService
from src.middleware.auth_middleware import get_current_user, require_roles

router = APIRouter()

def get_user_service() -> UserService:
    return UserService()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user"""
    try:
        user = user_service.create_user(user_data)
        return UserResponse(
            success=True, 
            user=user,
            message="User created successfully. Account is pending activation."
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred"
        )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """Get user by ID"""
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(success=True, user=user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    updates: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    """Update user"""
    try:
        user = user_service.update_user(user_id, updates)
        return UserResponse(
            success=True, 
            user=user,
            message="User updated successfully"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{user_id}/state", response_model=UserResponse)
async def change_user_state(
    user_id: str,
    state_update: UserStateUpdate,
    user_service: UserService = Depends(get_user_service)
):
    """Change user state (Admin only in production)"""
    try:
        user = user_service.change_user_state(user_id, state_update.state)
        return UserResponse(
            success=True, 
            user=user,
            message=f"User state changed to {state_update.state.value}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{user_id}/role", response_model=UserResponse)
async def assign_role(
    user_id: str,
    role_update: UserRoleUpdate,
    user_service: UserService = Depends(get_user_service)
):
    """Assign role to user (Admin only in production)"""
    try:
        user = user_service.assign_role(user_id, role_update.role)
        return UserResponse(
            success=True, 
            user=user,
            message=f"User role assigned to {role_update.role.value}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=UsersResponse)
async def list_users(
    role: Optional[str] = Query(None, description="Filter by role"),
    state: Optional[str] = Query(None, description="Filter by state"),
    email: Optional[str] = Query(None, description="Search by email"),
    user_service: UserService = Depends(get_user_service)
):
    """List users with optional filters"""
    filters = {}
    if role:
        filters['role'] = role
    if state:
        filters['state'] = state
    if email:
        filters['email'] = email
    
    users = user_service.list_users(filters)
    return UsersResponse(success=True, users=users, count=len(users))

@router.post("/auth/login", response_model=LoginResponse)
async def login(
    login_data: UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    """Authenticate user and return token"""
    user = user_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    if user.state != UserState.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account is {user.state.value.lower()}. Please contact administrator."
        )
    
    # Generate token
    token, expires_at = user_service.generate_token(user)
    
    return LoginResponse(
        success=True, 
        token=token, 
        user=user,
        expires_at=expires_at
    )

@router.post("/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """Activate a pending user account"""
    try:
        user = user_service.change_user_state(user_id, UserState.ACTIVE)
        return UserResponse(
            success=True,
            user=user,
            message="User account activated successfully"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
