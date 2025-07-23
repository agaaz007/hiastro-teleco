#!/usr/bin/env python3
"""
Voice Assistant Server Startup Script
"""
import os
import sys
import subprocess
import signal
import time

def get_ngrok_url():
    """Get the current ngrok URL"""
    try:
        result = subprocess.run(['curl', '-s', 'localhost:4040/api/tunnels'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            for tunnel in data.get('tunnels', []):
                if tunnel.get('proto') == 'https':
                    public_url = tunnel.get('public_url', '').replace('https://', 'wss://')
                    print(f"Found ngrok URL: {public_url}")
                    return public_url
    except Exception as e:
        print(f"Could not auto-detect ngrok URL: {e}")
    return None

def main():
    print("🎙️  Voice Assistant Server Startup")
    print("=" * 40)
    
    # Check if ngrok is running
    ngrok_url = get_ngrok_url()
    if ngrok_url:
        os.environ["NGROK_URL"] = ngrok_url
        print(f"✅ Using ngrok URL: {ngrok_url}")
    else:
        print("⚠️  Could not detect ngrok URL. Using default or environment variable.")
        if "NGROK_URL" in os.environ:
            print(f"   Using NGROK_URL: {os.environ['NGROK_URL']}")
        else:
            print("   Using hardcoded default URL")
    
    # Start the server
    print("\n🚀 Starting FastAPI server...")
    print("   Press Ctrl+C to stop")
    print("   Server will be available at: http://localhost:8000")
    print("   Twilio webhook: http://localhost:8000/twilio/voice")
    print("   WebSocket endpoint: ws://localhost:8000/ws/twilio")
    
    try:
        # Change to the parent directory to run the server
        os.chdir('..')
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'router.pipeline:app', 
            '--host', '0.0.0.0', 
            '--port', '8000',
            '--reload'
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 