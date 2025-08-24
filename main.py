#!/usr/bin/env python3
"""
Main entry point for the Farmer AI Agriculture Assistant
"""
import os
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

def main():
    """Main entry point"""
    try:
        from farmer import create_app, get_config
        from farmer.config.logging_config import get_logger
        
        logger = get_logger(__name__)
        logger.info("Starting Farmer AI Agriculture Assistant")
        
        # Get configuration
        config = get_config()
        
        # Create and run application
        app = create_app()
        
        logger.info(f"Server starting on {config.server.host}:{config.server.port}")
        logger.info(f"Debug mode: {'enabled' if config.server.debug else 'disabled'}")
        
        # Allow port override via environment variable
        port = int(os.getenv('PORT', config.server.port))
        
        app.run(
            host=config.server.host,
            port=port,
            debug=config.server.debug,
            threaded=config.server.threaded
        )
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to start Farmer: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
