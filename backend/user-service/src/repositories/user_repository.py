import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from src.models.user import User, UserRole, UserState
from src.database.connection import DatabaseManager

class UserRepository:
    def __init__(self):
        self.db = DatabaseManager()
    
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user"""
        query = '''
            INSERT INTO users (id, username, email, first_name, last_name, 
                             role, state, password_hash, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        try:
            self.db.execute_update(query, (
                user_data['id'], user_data['username'], user_data['email'],
                user_data['first_name'], user_data['last_name'], user_data['role'],
                user_data['state'], user_data['password_hash'],
                user_data['created_at'], user_data['updated_at']
            ))
            
            return self.get_user_by_id(user_data['id'])
        
        except sqlite3.IntegrityError as e:
            if "unique_username" in str(e).lower():
                raise ValueError("Username already exists")
            elif "unique_email" in str(e).lower():
                raise ValueError("Email already exists")
            else:
                raise ValueError("User creation failed: data integrity error")
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        query = 'SELECT * FROM users WHERE id = ?'
        rows = self.db.execute_query(query, (user_id,))
        
        if rows:
            return self._row_to_user(rows[0])
        return None
    
    def get_user_by_username(self, username: str) -> Optional[Tuple[User, str]]:
        """Get user by username with password hash"""
        query = 'SELECT * FROM users WHERE username = ?'
        rows = self.db.execute_query(query, (username.lower(),))
        
        if rows:
            row = rows[0]
            user = self._row_to_user(row)
            return user, row['password_hash']
        return None
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Optional[User]:
        """Update user with provided fields"""
        if not updates:
            return self.get_user_by_id(user_id)
        
        # Build dynamic update query
        fields = []
        values = []
        
        for key, value in updates.items():
            if key in ['username', 'email', 'first_name', 'last_name', 'password_hash', 'role', 'state']:
                fields.append(f"{key} = ?")
                values.append(value)
        
        if not fields:
            return self.get_user_by_id(user_id)
        
        # Add updated_at
        fields.append("updated_at = ?")
        values.append(datetime.now().isoformat())
        values.append(user_id)
        
        query = f'UPDATE users SET {", ".join(fields)} WHERE id = ?'
        
        try:
            rows_affected = self.db.execute_update(query, tuple(values))
            if rows_affected == 0:
                return None
            return self.get_user_by_id(user_id)
        except sqlite3.IntegrityError as e:
            if "unique_username" in str(e).lower():
                raise ValueError("Username already exists")
            elif "unique_email" in str(e).lower():
                raise ValueError("Email already exists")
            else:
                raise ValueError("Update failed: data integrity error")
    
    def list_users(self, filters: Dict[str, Any] = None) -> List[User]:
        """List users with optional filters"""
        query = "SELECT * FROM users"
        params = []
        
        if filters:
            conditions = []
            if 'role' in filters:
                conditions.append("role = ?")
                params.append(filters['role'])
            if 'state' in filters:
                conditions.append("state = ?")
                params.append(filters['state'])
            if 'email' in filters:
                conditions.append("email LIKE ?")
                params.append(f"%{filters['email']}%")
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        # Add ordering
        query += " ORDER BY created_at DESC"
        
        rows = self.db.execute_query(query, tuple(params))
        return [self._row_to_user(row) for row in rows]
    
    def _row_to_user(self, row: sqlite3.Row) -> User:
        """Convert database row to User model"""
        return User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            role=UserRole(row['role']),
            state=UserState(row['state']),
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at'])
        )