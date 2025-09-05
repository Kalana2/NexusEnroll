from .connection import DatabaseManager

__all__ = [
    'DatabaseManager'
]

# Version info
__version__ = '1.0.0'
__author__ = 'NexusEnroll Team'

# Database configuration
DB_CONFIG = {
    'default_db_path': 'data/users.db',
    'test_db_path': 'data/test_users.db',
    'backup_dir': 'data/backups/',
    'max_connections': 10,
    'timeout': 30.0
}