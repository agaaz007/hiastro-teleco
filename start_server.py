#!/usr/bin/env python3
"""
Startup script for Gemini Live API + Twilio voice assistant
"""
import os
import sys
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'scipy',
        'numpy',
        'soundfile',
        'librosa'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    # Special check for google.genai
    try:
        import google.genai
        print("✅ google.genai imported successfully")
    except ImportError:
        missing.append('google-generativeai')
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("Install them with: pip install " + " ".join(missing))
        return False
    
    return True

def check_env_vars():
    """Check if required environment variables are set"""
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY environment variable not set!")
        print("Get your API key from: https://aistudio.google.com/app/apikey")
        print("Then set it with: export GOOGLE_API_KEY='your-api-key-here'")
        return False
    
    return True

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "router.pipeline:app", 
            "--host", "0.0.0.0", 
            "--port", "9000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

if __name__ == "__main__":
    print("🔧 Checking setup...")
    
    if not check_dependencies():
        sys.exit(1)
    
    if not check_env_vars():
        sys.exit(1)
    
    print("✅ All checks passed!")
    print("📝 Make sure to:")
    print("   1. Start ngrok: ngrok http 9000")
    print("   2. Update Twilio webhook with your ngrok URL")
    print("   3. Update NGROK_URL in your .env file")
    print("")
    
    start_server() 