from typing import Dict, Any, List
import sqlite3
from datetime import datetime
from .connection import DatabaseManager

def log_user_action(user_id: str, action: str, old_values: Dict[str, Any] = None, 
                   new_values: Dict[str, Any] = None, changed_by: str = None,
                   ip_address: str = None):
    """
    Log user action to audit trail
    
    Args:
        user_id: ID of the user being modified
        action: Action performed (created, updated, deleted, etc.)
        old_values: Previous values (for updates)
        new_values: New values
        changed_by: ID of user making the change
        ip_address: IP address of the request
    """
    db = DatabaseManager()
    
    import json
    
    query = '''
        INSERT INTO user_audit_log (user_id, action, old_values, new_values, 
                                  changed_by, timestamp, ip_address)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    
    params = (
        user_id,
        action,
        json.dumps(old_values) if old_values else None,
        json.dumps(new_values) if new_values else None,
        changed_by,
        datetime.now().isoformat(),
        ip_address
    )
    
    db.execute_update(query, params)

def get_user_audit_log(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Get audit log for a specific user
    
    Args:
        user_id: ID of the user
        limit: Maximum number of records to return
        
    Returns:
        List of audit log entries
    """
    db = DatabaseManager()
    
    query = '''
        SELECT * FROM user_audit_log 
        WHERE user_id = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
    '''
    
    rows = db.execute_query(query, (user_id, limit))
    
    import json
    
    return [
        {
            'id': row['id'],
            'user_id': row['user_id'],
            'action': row['action'],
            'old_values': json.loads(row['old_values']) if row['old_values'] else None,
            'new_values': json.loads(row['new_values']) if row['new_values'] else None,
            'changed_by': row['changed_by'],
            'timestamp': row['timestamp'],
            'ip_address': row['ip_address']
        }
        for row in rows
    ]

def cleanup_old_audit_logs(days: int = 90):
    """
    Clean up audit logs older than specified days
    
    Args:
        days: Number of days to keep logs
    """
    db = DatabaseManager()
    
    from datetime import timedelta
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
    
    query = 'DELETE FROM user_audit_log WHERE timestamp < ?'
    rows_deleted = db.execute_update(query, (cutoff_date,))
    
    print(f"🧹 Cleaned up {rows_deleted} old audit log entries")
    return rows_deleted

def get_database_statistics() -> Dict[str, Any]:
    """Get comprehensive database statistics"""
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        stats = {}
        
        # User statistics by role
        role_stats = conn.execute('''
            SELECT role, COUNT(*) as count 
            FROM users 
            GROUP BY role
        ''').fetchall()
        stats['users_by_role'] = {row['role']: row['count'] for row in role_stats}
        
        # User statistics by state
        state_stats = conn.execute('''
            SELECT state, COUNT(*) as count 
            FROM users 
            GROUP BY state
        ''').fetchall()
        stats['users_by_state'] = {row['state']: row['count'] for row in state_stats}
        
        # Recent activity
        recent_users = conn.execute('''
            SELECT COUNT(*) as count 
            FROM users 
            WHERE created_at > datetime('now', '-7 days')
        ''').fetchone()
        stats['new_users_last_7_days'] = recent_users['count']
        
        # Audit log statistics
        audit_stats = conn.execute('''
            SELECT action, COUNT(*) as count 
            FROM user_audit_log 
            WHERE timestamp > datetime('now', '-30 days')
            GROUP BY action
        ''').fetchall()
        stats['recent_actions'] = {row['action']: row['count'] for row in audit_stats}
        
        return stats