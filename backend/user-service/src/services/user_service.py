import uuid
import hashlib
from datetime import datetime
from typing import List, Optional, Dict, Any
from src.models.user import (
    User,
    UserRole,
    UserState,
    UserCreate,
    UserUpdate,
    get_user_by_id,
    get_users,
    create_user,
    update_user,
    delete_user,
    authenticate_user,
)
from src.repositories.user_repository import UserRepository
from src.events.event_publisher import EventPublisher


class UserService:
    def __init__(self):
        self.repository = UserRepository()
        self.event_publisher = EventPublisher()

    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user"""
        user_create = UserCreate(**user_data)
        return create_user(user_create)

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return get_user_by_id(user_id)

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Optional[User]:
        """Update user with provided fields"""
        user_update = UserUpdate(**updates)
        return update_user(user_id, user_update)

    def delete_user(self, user_id: str) -> bool:
        """Delete user by ID"""
        return delete_user(user_id)

    def list_users(self, filters: Optional[Dict[str, Any]] = None) -> List[User]:
        """List users with optional filters"""
        # Only supports limit/offset for now; add filter logic if needed
        users, _ = get_users()
        if filters:
            if "role" in filters:
                users = [u for u in users if u.role == filters["role"]]
            if "state" in filters:
                users = [u for u in users if u.state == filters["state"]]
            if "email" in filters:
                users = [u for u in users if u.email == filters["email"]]
        return users

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user by username and password"""
        return authenticate_user(username, password)

    def change_user_state(self, user_id: str, state: str) -> Optional[User]:
        """Change user state"""
        return self.update_user(user_id, {"state": state})

    def assign_role(self, user_id: str, role: str) -> Optional[User]:
        """Assign role to user"""
        return self.update_user(user_id, {"role": role})
