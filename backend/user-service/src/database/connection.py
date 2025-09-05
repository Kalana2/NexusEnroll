import sqlite3
import os
import shutil
from typing import Optional
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime

class DatabaseManager:
    """
    Singleton database manager for SQLite operations
    
    Features:
    - Connection pooling simulation
    - Automatic schema creation
    - Database backup utilities
    - Transaction management
    """
    
    _instance: Optional['DatabaseManager'] = None
    
    def __new__(cls, db_path: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, db_path: str = None):
        if self._initialized:
            return
            
        self.db_path = db_path or "data/users.db"
        self.backup_dir = "data/backups"
        self._connection_count = 0
        
        self._ensure_directories()
        self._init_database()
        self._initialized = True
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        data_dir = Path(self.db_path).parent
        backup_dir = Path(self.backup_dir)
        
        data_dir.mkdir(exist_ok=True)
        backup_dir.mkdir(exist_ok=True)
        
        print(f"✅ Database directories ensured: {data_dir}")
    
    def _init_database(self):
        """Initialize database with complete schema"""
        with self.get_connection() as conn:
            # Enable foreign key support
            conn.execute('PRAGMA foreign_keys = ON')
            
            # Create users table with all constraints
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL COLLATE NOCASE,
                    email TEXT UNIQUE NOT NULL COLLATE NOCASE,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('Student', 'Faculty', 'Admin')),
                    state TEXT NOT NULL CHECK(state IN ('Active', 'Suspended', 'Pending')),
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    last_login_at TEXT,
                    login_attempts INTEGER DEFAULT 0,
                    locked_until TEXT
                )
            ''')
            
            # Create indexes for better performance
            self._create_indexes(conn)
            
            # Create audit log table for tracking changes
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    old_values TEXT,
                    new_values TEXT,
                    changed_by TEXT,
                    timestamp TEXT NOT NULL,
                    ip_address TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            conn.commit()
            print("✅ Database schema initialized successfully")
    
    def _create_indexes(self, conn: sqlite3.Connection):
        """Create database indexes for performance"""
        indexes = [
            'CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)',
            'CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)',
            'CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)',
            'CREATE INDEX IF NOT EXISTS idx_users_state ON users(state)',
            'CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at)',
            'CREATE INDEX IF NOT EXISTS idx_users_last_login ON users(last_login_at)',
            'CREATE INDEX IF NOT EXISTS idx_audit_user_id ON user_audit_log(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON user_audit_log(timestamp)'
        ]
        
        for index_sql in indexes:
            conn.execute(index_sql)
        
        print("✅ Database indexes created")
    
    @contextmanager
    def get_connection(self):
        """
        Get database connection with proper cleanup
        
        Usage:
            with db.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM users")
        """
        self._connection_count += 1
        conn = sqlite3.connect(
            self.db_path,
            timeout=30.0,
            check_same_thread=False
        )
        conn.row_factory = sqlite3.Row
        
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            self._connection_count -= 1
    
    @contextmanager
    def get_transaction(self):
        """
        Get database connection with automatic transaction management
        
        Usage:
            with db.get_transaction() as conn:
                conn.execute("INSERT ...")
                conn.execute("UPDATE ...")
                # Automatically commits on success, rolls back on error
        """
        with self.get_connection() as conn:
            try:
                conn.execute('BEGIN TRANSACTION')
                yield conn
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
    
    def execute_query(self, query: str, params: tuple = ()) -> list:
        """Execute a SELECT query and return results"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return rows affected"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    def execute_many(self, query: str, params_list: list) -> int:
        """Execute multiple queries with different parameters"""
        with self.get_connection() as conn:
            cursor = conn.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount
    
    def backup_database(self, backup_name: str = None) -> str:
        """
        Create a backup of the database
        
        Args:
            backup_name: Optional custom backup name
            
        Returns:
            Path to the backup file
        """
        if not backup_name:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"users_backup_{timestamp}.db"
        
        backup_path = Path(self.backup_dir) / backup_name
        
        try:
            shutil.copy2(self.db_path, backup_path)
            print(f"✅ Database backup created: {backup_path}")
            return str(backup_path)
        except Exception as e:
            print(f"❌ Database backup failed: {e}")
            raise
    
    def restore_database(self, backup_path: str):
        """
        Restore database from backup
        
        Args:
            backup_path: Path to the backup file
        """
        if not Path(backup_path).exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        try:
            # Create backup of current database before restore
            current_backup = self.backup_database("pre_restore_backup.db")
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            
            print(f"✅ Database restored from: {backup_path}")
            print(f"📝 Previous database backed up to: {current_backup}")
            
        except Exception as e:
            print(f"❌ Database restore failed: {e}")
            raise
    
    def get_database_info(self) -> dict:
        """Get database information and statistics"""
        with self.get_connection() as conn:
            # Get database size
            db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            
            # Get table counts
            user_count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
            audit_count = conn.execute('SELECT COUNT(*) FROM user_audit_log').fetchone()[0]
            
            # Get database version
            db_version = conn.execute('PRAGMA user_version').fetchone()[0]
            
            return {
                'database_path': self.db_path,
                'database_size_bytes': db_size,
                'database_size_mb': round(db_size / (1024 * 1024), 2),
                'user_count': user_count,
                'audit_log_count': audit_count,
                'database_version': db_version,
                'active_connections': self._connection_count,
                'tables': self._get_table_list(conn)
            }
    
    def _get_table_list(self, conn: sqlite3.Connection) -> list:
        """Get list of all tables in the database"""
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        return [row[0] for row in cursor.fetchall()]
    
    def vacuum_database(self):
        """Optimize database by reclaiming unused space"""
        try:
            with self.get_connection() as conn:
                conn.execute('VACUUM')
                print("✅ Database vacuum completed")
        except Exception as e:
            print(f"❌ Database vacuum failed: {e}")
            raise
    
    def check_database_integrity(self) -> bool:
        """Check database integrity"""
        try:
            with self.get_connection() as conn:
                result = conn.execute('PRAGMA integrity_check').fetchone()
                is_ok = result[0] == 'ok'
                
                if is_ok:
                    print("✅ Database integrity check passed")
                else:
                    print(f"❌ Database integrity check failed: {result[0]}")
                
                return is_ok
                
        except Exception as e:
            print(f"❌ Database integrity check error: {e}")
            return False
    
    def close(self):
        """Close database manager (cleanup method)"""
        if hasattr(self, '_initialized') and self._initialized:
            print(f"📝 Database manager closed. Final connection count: {self._connection_count}")
            self._initialized = False