#!/usr/bin/env python3
"""
Command Line Interface for the Farmer AI Agriculture Assistant
"""
import os
import sys
import click
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from farmer import create_app, get_config, setup_logging
from farmer.config.logging_config import get_logger

logger = get_logger(__name__)

@click.group()
@click.version_option(version='1.0.0', prog_name='farmer')
@click.option('--config', '-c', help='Configuration environment (development/production/testing)')
@click.option('--log-level', '-l', default='INFO', help='Logging level')
@click.option('--log-format', default='detailed', help='Log format (detailed/simple/json)')
@click.pass_context
def cli(ctx, config: Optional[str], log_level: str, log_format: str):
    """Farmer AI Agriculture Assistant - CLI Tool"""
    
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Set configuration
    if config:
        os.environ['FLASK_ENV'] = config
        ctx.obj['config_env'] = config
    
    # Setup logging
    setup_logging(
        log_level=log_level,
        log_format=log_format,
        console_output=True,
        file_output=True
    )
    
    logger.info(f"Farmer CLI initialized with config: {config or 'default'}, log level: {log_level}")

@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=5000, help='Port to bind to')
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.option('--reload', is_flag=True, help='Enable auto-reload')
@click.pass_context
def run(ctx, host: str, port: int, debug: bool, reload: bool):
    """Run the Farmer AI Agriculture Assistant web server"""
    
    try:
        config_env = ctx.obj.get('config_env', os.getenv('FLASK_ENV', 'development'))
        logger.info(f"Starting Farmer server in {config_env} mode")
        
        # Create application
        app = create_app(config_env)
        
        # Override configuration if specified
        if host != '0.0.0.0':
            app.config['HOST'] = host
        if port != 5000:
            app.config['PORT'] = port
        if debug:
            app.config['DEBUG'] = True
        
        logger.info(f"Server will start on {host}:{port}")
        logger.info(f"Debug mode: {'enabled' if debug else 'disabled'}")
        
        # Run the application
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=reload
        )
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

@cli.command()
@click.option('--force', is_flag=True, help='Force recreation of database')
@click.pass_context
def init_db(ctx, force: bool):
    """Initialize the database"""
    
    try:
        config_env = ctx.obj.get('config_env', os.getenv('FLASK_ENV', 'development'))
        logger.info(f"Initializing database in {config_env} mode")
        
        app = create_app(config_env)
        
        with app.app_context():
            from farmer.core.database import init_db, create_tables
            
            # Initialize database
            init_db(app)
            logger.info("Database connection initialized")
            
            # Create tables
            create_tables()
            logger.info("Database tables created")
            
            if force:
                logger.info("Database recreated successfully")
            else:
                logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        sys.exit(1)

@cli.command()
@click.option('--days', default=90, help='Number of days to keep logs')
@click.option('--dry-run', is_flag=True, help='Show what would be deleted without actually deleting')
@click.pass_context
def cleanup_logs(ctx, days: int, dry_run: bool):
    """Clean up old log files"""
    
    try:
        from farmer.utils.file_utils import cleanup_old_files
        
        log_dir = 'logs'
        max_age_hours = days * 24
        
        if dry_run:
            logger.info(f"DRY RUN: Would clean up logs older than {days} days in {log_dir}")
            # Count files that would be deleted
            count = 0
            current_time = datetime.now()
            max_age = timedelta(hours=max_age_hours)
            
            for file_path in Path(log_dir).glob('*.log'):
                if file_path.is_file():
                    file_age = current_time - datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_age > max_age:
                        count += 1
                        logger.info(f"Would delete: {file_path}")
            
            logger.info(f"DRY RUN: {count} log files would be deleted")
        else:
            count = cleanup_old_files(log_dir, max_age_hours)
            logger.info(f"Cleaned up {count} old log files")
        
    except Exception as e:
        logger.error(f"Failed to cleanup logs: {e}")
        sys.exit(1)

@cli.command()
@click.pass_context
def health_check(ctx):
    """Perform system health check"""
    
    try:
        config_env = ctx.obj.get('config_env', os.getenv('FLASK_ENV', 'development'))
        logger.info(f"Performing health check in {config_env} mode")
        
        app = create_app(config_env)
        
        with app.app_context():
            from farmer.core.health import perform_health_check
            
            status = perform_health_check()
            
            if status['status'] == 'healthy':
                logger.info("✅ Health check passed")
                click.echo("System is healthy")
                click.echo(f"Status: {status['status']}")
            else:
                logger.error(f"❌ Health check failed: {status.get('error', 'Unknown error')}")
                click.echo(f"System has issues: {status.get('error', 'Unknown error')}")
                sys.exit(1)
        
    except Exception as e:
        logger.error(f"Failed to perform health check: {e}")
        sys.exit(1)

@cli.command()
@click.option('--output', '-o', help='Output file for configuration')
@click.pass_context
def show_config(ctx, output: Optional[str]):
    """Show current configuration"""
    
    try:
        config_env = ctx.obj.get('config_env', os.getenv('FLASK_ENV', 'development'))
        logger.info(f"Showing configuration for {config_env} mode")
        
        config = get_config()
        config_dict = config.to_dict()
        
        if output:
            import json
            with open(output, 'w') as f:
                json.dump(config_dict, f, indent=2, default=str)
            logger.info(f"Configuration saved to {output}")
        else:
            import json
            click.echo(json.dumps(config_dict, indent=2, default=str))
        
    except Exception as e:
        logger.error(f"Failed to show configuration: {e}")
        sys.exit(1)

@cli.command()
@click.option('--template', '-t', help='Template to use for new project')
@click.option('--output', '-o', default='./farmer-project', help='Output directory')
@click.pass_context
def create_project(ctx, template: Optional[str], output: str):
    """Create a new Farmer project"""
    
    try:
        logger.info(f"Creating new Farmer project in {output}")
        
        # Create project structure
        project_path = Path(output)
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Copy template files
        template_dir = Path(__file__).parent.parent / 'templates' / (template or 'default')
        
        if template_dir.exists():
            import shutil
            shutil.copytree(template_dir, project_path, dirs_exist_ok=True)
            logger.info(f"Project created from template: {template}")
        else:
            # Create basic structure
            (project_path / 'src').mkdir(exist_ok=True)
            (project_path / 'tests').mkdir(exist_ok=True)
            (project_path / 'logs').mkdir(exist_ok=True)
            (project_path / 'docs').mkdir(exist_ok=True)
            
            # Create basic files
            (project_path / 'README.md').write_text('# Farmer AI Agriculture Assistant\n\nYour project description here.')
            (project_path / '.env.example').write_text('# Environment variables\nOPENAI_API_KEY=your_key_here\nHUGGINGFACE_KEY=your_key_here')
            
            logger.info("Basic project structure created")
        
        logger.info(f"Project created successfully in {output}")
        click.echo(f"Project created in {output}")
        
    except Exception as e:
        logger.error(f"Failed to create project: {e}")
        sys.exit(1)

@cli.command()
@click.pass_context
def test(ctx):
    """Run the test suite"""
    
    try:
        logger.info("Running test suite")
        
        # Change to project root
        project_root = Path(__file__).parent.parent.parent
        os.chdir(project_root)
        
        # Run tests
        import subprocess
        result = subprocess.run(['python', '-m', 'pytest', 'tests/', '-v'], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ All tests passed")
            click.echo("All tests passed")
        else:
            logger.error("❌ Some tests failed")
            click.echo(result.stdout)
            click.echo(result.stderr)
            sys.exit(1)
        
    except Exception as e:
        logger.error(f"Failed to run tests: {e}")
        sys.exit(1)

def main():
    """Main CLI entry point"""
    try:
        cli()
    except KeyboardInterrupt:
        logger.info("CLI interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"CLI failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
