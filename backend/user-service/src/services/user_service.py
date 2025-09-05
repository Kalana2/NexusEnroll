import uuid
import hashlib
from datetime import datetime
from typing import List, Optional, Dict, Any
from src.models.user import User, UserRole, UserState
from src.repositories.user_repository import UserRepository
from src.events.event_publisher import EventPublisher

class UserService:
    def __init__(self):
        self.repository = UserRepository()
        self.event_publisher = EventPublisher()
    
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user"""
        # Validate required fields
        required_fields = ['username', 'email', 'first_name', 'last_name', 'password']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Check if username or email already exists
        if self.repository.get_user_by_username(user_data['username']):
            raise ValueError("Username already exists")
        
        # Hash password
        password_hash = self._hash_password(user_data['password'])
        
        # Create user object
        user = User(
            id=str(uuid.uuid4()),
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            role=UserRole(user_data.get('role', 'Student')),
            state=UserState.PENDING,  # New users start as pending
            created_at=datetime.now(),
            updated_at=datetime.now(),
            password_hash=password_hash
        )
        
        # Save to database
        created_user = self.repository.create_user(user)
        
        # Publish event
        self.event_publisher.publish('user.created', {
            'user_id': created_user.id,
            'username': created_user.username,
            'email': created_user.email,
            'role': created_user.role.value,
            'state': created_user.state.value
        })
        
        return created_user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.repository.get_user_by_id(user_id)
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Optional[User]:
        """Update user with provided fields"""
        # Get current user
        current_user = self.repository.get_user_by_id(user_id)
        if not current_user:
            raise ValueError("User not found")
        
        # Hash password if provided
        if 'password' in updates:
            updates['password_hash'] = self._hash_password(updates['password'])
            del updates['password']
        
        # Convert role/state strings to enums if provided
        if 'role' in updates and isinstance(updates['role'], str):
            updates['role'] = UserRole(updates['role'])
        if 'state' in updates and isinstance(updates['state'], str):
            updates['state'] = UserState(updates['state'])
        
        # Update user
        updated_user = self.repository.update_user(user_id, updates)
        
        # Publish event if role or state changed
        if 'role' in updates or 'state' in updates:
            self.event_publisher.publish('user.updated', {
                'user_id': updated_user.id,
                'username': updated_user.username,
                'role': updated_user.role.value,
                'state': updated_user.state.value,
                'changes': list(updates.keys())
            })
        
        return updated_user
    
    def change_user_state(self, user_id: str, state: str) -> User:
        """Change user state (Active/Suspended/Pending)"""
        user_state = UserState(state)
        updated_user = self.update_user(user_id, {'state': user_state})
        
        if not updated_user:
            raise ValueError("User not found")
        
        # Publish specific state change event
        self.event_publisher.publish('user.state_changed', {
            'user_id': updated_user.id,
            'username': updated_user.username,
            'new_state': state,
            'timestamp': datetime.now().isoformat()
        })
        
        return updated_user
    
    def assign_role(self, user_id: str, role: str) -> User:
        """Assign role to user (Student/Faculty/Admin)"""
        user_role = UserRole(role)
        updated_user = self.update_user(user_id, {'role': user_role})
        
        if not updated_user:
            raise ValueError("User not found")
        
        # Publish role assignment event
        self.event_publisher.publish('user.role_assigned', {
            'user_id': updated_user.id,
            'username': updated_user.username,
            'new_role': role,
            'timestamp': datetime.now().isoformat()
        })
        
        return updated_user
    
    def list_users(self, filters: Dict[str, Any] = None) -> List[User]:
        """List users with optional filters"""
        return self.repository.list_users(filters or {})
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user by username and password"""
        user = self.repository.get_user_by_username(username)
        if user and self._verify_password(password, user.password_hash):
            return user
        return None
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256 (use bcrypt in production)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return self._hash_password(password) == password_hash