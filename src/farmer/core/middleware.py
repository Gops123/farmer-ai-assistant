"""
Middleware for request/response handling
"""
from flask import request, g, current_app
import time
import logging

logger = logging.getLogger(__name__)

def setup_middleware(app):
    """Setup middleware for the Flask app"""
    
    @app.before_request
    def before_request():
        """Log request details and start timing"""
        g.start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
        
        # Log request headers for debugging
        if current_app.config.get('FARMER_DEBUG', False):
            logger.debug(f"Request headers: {dict(request.headers)}")
    
    @app.after_request
    def after_request(response):
        """Log response details and timing"""
        if hasattr(g, 'start_time'):
            duration = (time.time() - g.start_time) * 1000  # Convert to milliseconds
            logger.info(f"Response: {response.status_code} in {duration:.2f}ms")
        else:
            logger.info(f"Response: {response.status_code}")
        
        return response
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        logger.warning(f"404 error: {request.path}")
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logger.error(f"500 error: {error}")
        return {'error': 'Internal server error'}, 500
