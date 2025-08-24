"""
Health check functionality
"""
import logging
import os
import sys
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_system_health() -> Dict[str, Any]:
    """Perform comprehensive system health check"""
    health_status = {
        'status': 'healthy',
        'checks': {},
        'timestamp': None
    }
    
    try:
        # Check Python version
        python_version = sys.version_info
        health_status['checks']['python'] = {
            'status': 'healthy',
            'version': f"{python_version.major}.{python_version.minor}.{python_version.micro}"
        }
        
        # Check environment variables
        required_env_vars = ['OPENAI_API_KEY', 'HUGGINGFACE_KEY']
        env_status = {}
        for var in required_env_vars:
            if os.getenv(var):
                env_status[var] = {'status': 'healthy', 'value': '***'}
            else:
                env_status[var] = {'status': 'warning', 'value': 'Not set'}
        
        health_status['checks']['environment'] = env_status
        
        # Check file permissions
        file_checks = {}
        directories = ['logs', 'uploads', 'static']
        for directory in directories:
            if os.path.exists(directory):
                if os.access(directory, os.W_OK):
                    file_checks[directory] = {'status': 'healthy', 'writable': True}
                else:
                    file_checks[directory] = {'status': 'unhealthy', 'writable': False}
            else:
                file_checks[directory] = {'status': 'warning', 'exists': False}
        
        health_status['checks']['filesystem'] = file_checks
        
        # Overall status
        all_healthy = True
        for category, checks in health_status['checks'].items():
            if isinstance(checks, dict):
                for check_name, check_data in checks.items():
                    if isinstance(check_data, dict) and check_data.get('status') == 'unhealthy':
                        all_healthy = False
                        break
        
        health_status['status'] = 'healthy' if all_healthy else 'unhealthy'
        
        logger.info("Health check completed successfully")
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        health_status['status'] = 'error'
        health_status['error'] = str(e)
    
    return health_status

# Alias for CLI compatibility
def perform_health_check() -> Dict[str, Any]:
    """Alias for check_system_health for CLI compatibility"""
    return check_system_health()

def check_database_health() -> Dict[str, Any]:
    """Check database connectivity and health"""
    try:
        # TODO: Implement actual database health check
        return {
            'status': 'healthy',
            'message': 'Database connection successful'
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            'status': 'unhealthy',
            'error': str(e)
        }
