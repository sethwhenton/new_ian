#!/usr/bin/python3
"""
Development Startup Script for AI Object Counting Application
"""
import os
import sys
import logging
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def setup_development_environment():
    """Setup development environment"""
    # Set development environment
    os.environ['OBJ_DETECT_ENV'] = 'development'
    os.environ['OBJ_DETECT_MYSQL_DB'] = 'dev_obj_detect.db'
    os.environ['FLASK_DEBUG'] = 'True'
    os.environ['LOG_LEVEL'] = 'DEBUG'
    
    print("✅ Development environment configured")

def setup_directories():
    """Create necessary directories for development"""
    directories = [
        'dev_media',
        'logs',
        'models'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Directory created/verified: {directory}")

def setup_logging():
    """Setup development logging"""
    # Create logs directory
    Path('logs').mkdir(exist_ok=True)
    
    # Configure logging for development
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/dev_app.log'),
            logging.StreamHandler()
        ]
    )
    
    print("✅ Development logging configured")

def check_ai_models():
    """Check AI model availability"""
    try:
        from src.pipeline.pipeline import pipeline
        status = pipeline.get_model_status()
        
        if status.get('models_loaded', False):
            print("✅ AI models loaded successfully")
            print(f"   Device: {status.get('device', 'unknown')}")
            print(f"   SAM Model: {'✅' if status.get('sam_loaded') else '❌'}")
            print(f"   Classifier: {'✅' if status.get('classifier_loaded') else '❌'}")
        else:
            print("⚠️  AI models not loaded - this is expected in development")
            print("   Models will be downloaded on first use")
        
        return True
    except Exception as e:
        print(f"⚠️  AI model check failed: {e}")
        print("   This is normal in development - models will be downloaded when needed")
        return True

def start_development_server():
    """Start the development server"""
    try:
        from src.app import app
        from src.config import config
        
        print("🚀 Starting AI Object Counting Application (Development Mode)...")
        print(f"   Environment: {config.ENV}")
        print(f"   Host: {config.HOST}")
        print(f"   Port: {config.PORT}")
        print(f"   Database: {config.DATABASE_TYPE} ({config.DATABASE_PATH})")
        print(f"   Debug: {config.DEBUG}")
        print(f"   Media Directory: {config.MEDIA_DIRECTORY}")
        
        print("\n📋 Available Endpoints:")
        print("   - GET  /health - Health check")
        print("   - GET  /api/object - Object types")
        print("   - POST /api/count - Single image processing")
        print("   - POST /api/count-all - Auto-detection")
        print("   - POST /api/batch/process - Batch processing")
        print("   - GET  /api/output - Results")
        print("   - GET  /api/performance/* - Performance monitoring")
        
        print("\n🌐 Frontend Development Server:")
        print("   Run 'npm run dev' in seth_front_end/ directory")
        print("   Frontend will be available at http://localhost:3000")
        
        print("\n" + "=" * 60)
        print("🎉 Development server starting...")
        print("=" * 60)
        
        # Start the application
        app.run(
            host=config.HOST,
            port=config.PORT,
            threaded=True,
            debug=config.DEBUG
        )
        
    except Exception as e:
        logging.error(f"Failed to start development server: {e}")
        print(f"❌ Failed to start development server: {e}")
        sys.exit(1)

def main():
    """Main development startup function"""
    print("🔧 AI Object Counting Application - Development Startup")
    print("=" * 60)
    
    # Setup steps
    setup_development_environment()
    setup_directories()
    setup_logging()
    check_ai_models()
    
    print("\n🎉 Development environment ready!")
    print("=" * 60)
    
    # Start the development server
    start_development_server()

if __name__ == "__main__":
    main()



