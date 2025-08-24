"""
Main Flask application factory for the Farmer AI Agriculture Assistant
"""
import os
import time
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

from flask import Flask, request, g, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename

from .config.settings import get_config, config
from .config.logging_config import get_logger, setup_logging, log_api_request, log_api_response
from .models import Base
from .api.routes import api_bp
from .core.database import init_db
from .core.redis_client import init_redis
from .core.middleware import setup_middleware

logger = get_logger(__name__)

def create_app(config_name: Optional[str] = None, test_config: Optional[Dict[str, Any]] = None) -> Flask:
    """
    Create and configure the Flask application
    
    Args:
        config_name: Configuration environment name
        test_config: Test configuration dictionary
    
    Returns:
        Configured Flask application
    """
    logger.info("Creating Flask application")
    
    # Create Flask app
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder='../../templates',
        static_folder='../../static'
    )
    
    # Configure upload folder
    app.config['UPLOAD_FOLDER'] = '../../uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Load configuration
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_object('farmer.config.settings')
        
        # Override with environment-specific config
        if config_name:
            app.config.from_object(f'farmer.config.settings.{config_name.capitalize()}Config')
    else:
        # Load the test config if passed in
        app.config.update(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Setup logging
    setup_logging(
        log_level=config.logging.level,
        log_format=config.logging.format,
        log_dir=config.logging.directory,
        console_output=config.logging.console_output,
        file_output=config.logging.file_output,
        json_format=config.logging.json_format
    )
    
    # Validate configuration
    if not config.validate():
        logger.error("Configuration validation failed")
        raise RuntimeError("Invalid configuration")
    
    # Apply Flask configuration
    flask_config = config.get_flask_config()
    app.config.update(flask_config)
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Setup middleware
    setup_middleware(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register request handlers
    register_request_handlers(app)
    
    # Register CLI commands
    register_cli_commands(app)
    
    logger.info("Flask application created successfully")
    return app

def init_extensions(app: Flask) -> None:
    """Initialize Flask extensions"""
    logger.debug("Initializing Flask extensions")
    
    # Initialize database
    init_db(app)
    
    # Initialize Redis
    init_redis()
    
    # Initialize other extensions here as needed
    # Example: init_cache(app), init_celery(app), etc.

def register_blueprints(app: Flask) -> None:
    """Register Flask blueprints"""
    logger.debug("Registering Flask blueprints")
    
    # Register API blueprint
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Register main web routes
    @app.route('/')
    def index():
        """Serve the main application page"""
        # Template variables
        template_vars = {
            'languages': {
                'en': 'English',
                'es': 'Español',
                'fr': 'Français',
                'de': 'Deutsch',
                'hi': 'हिंदी',
                'zh': '中文',
                'ar': 'العربية'
            },
            'app_name': 'Farmer AI',
            'app_description': 'Your AI Agriculture Assistant'
        }
        return render_template('index.html', **template_vars)
    
    @app.route('/health')
    def health():
        """Simple health check endpoint"""
        return jsonify({'status': 'healthy', 'service': 'Farmer AI Agriculture Assistant'})
    
    @app.route('/chat', methods=['GET', 'POST'])
    def chat():
        """Handle chat messages and image uploads"""
        try:
            # Handle GET requests (for debugging)
            if request.method == 'GET':
                return jsonify({
                    'message': 'Chat endpoint is working!',
                    'method': 'GET',
                    'note': 'Use POST method for sending messages or uploading images'
                })
            
            # Check if it's an image upload
            if 'image' in request.files:
                file = request.files['image']
                if file.filename == '':
                    return jsonify({'error': 'No file selected'}), 400
                
                # Save the uploaded image
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # TODO: Implement actual image analysis with AI
                response_text = f"Image '{filename}' uploaded successfully! This appears to be a healthy crop image. For detailed disease analysis, please ensure the image shows clear details of any affected areas."
                
                return jsonify({
                    'text': response_text,
                    'filename': filename
                })
            
            # Handle text chat - support both JSON and form data
            if request.is_json:
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'No data provided'}), 400
                message = data.get('text', '')
            else:
                # Handle form data
                message = request.form.get('text', '')
            
            if not message:
                return jsonify({'error': 'Message is required'}), 400
            
            # TODO: Implement actual AI chat logic
            response_text = f"Thank you for your message: '{message}'. I'm here to help with agriculture advice. This is a demo response - in production, this would connect to OpenAI or other AI services."
            
            return jsonify({
                'text': response_text
            })
            
        except Exception as e:
            logger.error(f"Chat endpoint error: {e}")
            return jsonify({
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
    @app.route('/weather')
    def weather():
        """Get weather information for a location"""
        try:
            location = request.args.get('location', '')
            if not location:
                return jsonify({'error': 'Location is required'}), 400
            
            # TODO: Implement actual weather API integration
            # For now, return mock data
            mock_weather = {
                'location': location,
                'temperature': 25,
                'description': 'Sunny',
                'humidity': 65,
                'wind_speed': 12
            }
            
            return jsonify(mock_weather)
            
        except Exception as e:
            logger.error(f"Weather endpoint error: {e}")
            return jsonify({
                'error': 'Unable to fetch weather data',
                'message': str(e)
            }), 500
    
    @app.route('/crops')
    def crops():
        """Get crop recommendations"""
        try:
            location = request.args.get('location', '')
            soil_type = request.args.get('soil_type', '')
            
            if not location:
                return jsonify({'error': 'Location is required'}), 400
            
            # TODO: Implement actual crop recommendation logic
            # For now, return mock data
            mock_recommendations = {
                'weather': {
                    'temperature': 28,
                    'humidity': 70
                },
                'recommendations': [
                    'Wheat - Good for current conditions',
                    'Corn - Suitable for your soil type',
                    'Soybeans - Recommended for this season'
                ],
                'soil_info': f'Based on {soil_type or "mixed"} soil type in {location}'
            }
            
            return jsonify(mock_recommendations)
            
        except Exception as e:
            logger.error(f"Crops endpoint error: {e}")
            return jsonify({
                'error': 'Unable to get crop recommendations',
                'message': str(e)
            }), 500
    
    @app.route('/market')
    def market():
        """Get market prices"""
        try:
            # TODO: Implement actual market data integration
            # For now, return mock data
            mock_prices = {
                'wheat': {'price': '$5.50/bushel', 'trend': '↗️ +2.3%'},
                'corn': {'price': '$4.20/bushel', 'trend': '↘️ -1.1%'},
                'soybeans': {'price': '$12.80/bushel', 'trend': '↗️ +0.8%'},
                'rice': {'price': '$18.50/hundredweight', 'trend': '→ 0.0%'}
            }
            
            return jsonify(mock_prices)
            
        except Exception as e:
            logger.error(f"Market endpoint error: {e}")
            return jsonify({
                'error': 'Unable to load market prices',
                'message': str(e)
            }), 500
    
    @app.route('/export')
    def export_chat():
        """Export chat history"""
        try:
            # TODO: Implement actual chat export
            return jsonify({
                'message': 'Chat export feature coming soon!',
                'status': 'not_implemented'
            })
            
        except Exception as e:
            logger.error(f"Export endpoint error: {e}")
            return jsonify({
                'error': 'Unable to export chat',
                'message': str(e)
            }), 500
    
    # Register other blueprints here
    # Example: app.register_blueprint(web_bp), app.register_blueprint(admin_bp), etc.

def register_error_handlers(app: Flask) -> None:
    """Register error handlers"""
    logger.debug("Registering error handlers")
    
    @app.errorhandler(400)
    def bad_request(error):
        logger.warning(f"Bad request: {error}")
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request could not be processed',
            'timestamp': datetime.utcnow().isoformat()
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"Not found: {request.url}")
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'timestamp': datetime.utcnow().isoformat()
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'timestamp': datetime.utcnow().isoformat()
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Unhandled exception: {error}", exc_info=True)
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

def register_request_handlers(app: Flask) -> None:
    """Register request handlers for logging and monitoring"""
    logger.debug("Registering request handlers")
    
    @app.before_request
    def before_request():
        """Log request details and start timing"""
        g.start_time = time.time()
        g.request_id = f"req_{int(time.time() * 1000)}"
        
        # Log request
        log_api_request(
            logger,
            method=request.method,
            endpoint=request.endpoint or request.path,
            user_id=getattr(g, 'user_id', None),
            request_id=g.request_id,
            ip=request.remote_addr,
            user_agent=request.user_agent.string if request.user_agent else None
        )
    
    @app.after_request
    def after_request(response):
        """Log response details and timing"""
        if hasattr(g, 'start_time'):
            response_time = (time.time() - g.start_time) * 1000  # Convert to milliseconds
            
            # Log response
            try:
                content_length = len(response.get_data())
            except Exception:
                content_length = 0
                
            log_api_response(
                logger,
                method=request.method,
                endpoint=request.endpoint or request.path,
                status_code=response.status_code,
                response_time=response_time,
                request_id=getattr(g, 'request_id', None),
                content_length=content_length
            )
            
            # Add response time header
            response.headers['X-Response-Time'] = f"{response_time:.2f}ms"
        
        return response
    
    @app.teardown_request
    def teardown_request(exception=None):
        """Clean up request context"""
        if exception:
            logger.error(f"Request failed: {exception}", exc_info=True)
        
        # Clean up request context
        if hasattr(g, 'start_time'):
            del g.start_time
        if hasattr(g, 'request_id'):
            del g.request_id

def register_cli_commands(app: Flask) -> None:
    """Register CLI commands"""
    logger.debug("Registering CLI commands")
    
    @app.cli.command('init-db')
    def init_db_command():
        """Initialize the database."""
        from .core.database import init_db
        init_db(app)
        logger.info("Database initialized successfully")
    
    @app.cli.command('create-tables')
    def create_tables_command():
        """Create database tables."""
        from .core.database import create_tables
        create_tables()
        logger.info("Database tables created successfully")
    
    @app.cli.command('seed-data')
    def seed_data_command():
        """Seed database with initial data."""
        from .core.seeder import seed_database
        seed_database()
        logger.info("Database seeded successfully")
    
    @app.cli.command('cleanup-logs')
    def cleanup_logs_command():
        """Clean up old log files."""
        from .utils.file_utils import cleanup_old_files
        count = cleanup_old_files('logs', max_age_hours=24*7)  # 7 days
        logger.info(f"Cleaned up {count} old log files")
    
    @app.cli.command('health-check')
    def health_check_command():
        """Perform system health check."""
        from .core.health import perform_health_check
        status = perform_health_check()
        if status['healthy']:
            logger.info("Health check passed")
        else:
            logger.error(f"Health check failed: {status['issues']}")

def create_development_app() -> Flask:
    """Create development application"""
    return create_app('development')

def create_production_app() -> Flask:
    """Create production application"""
    return create_app('production')

def create_testing_app() -> Flask:
    """Create testing application"""
    return create_app('testing')

# Application factory for different environments
app_factories = {
    'development': create_development_app,
    'production': create_production_app,
    'testing': create_testing_app,
    'default': create_development_app
}

def get_app_factory(env: str = None) -> callable:
    """Get the appropriate app factory for the environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    
    return app_factories.get(env, app_factories['default'])

# For direct execution
if __name__ == '__main__':
    app = create_app()
    app.run(
        host=config.server.host,
        port=config.server.port,
        debug=config.server.debug,
        threaded=config.server.threaded
    )
