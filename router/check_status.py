#!/usr/bin/env python3
"""
Voice Assistant Status Checker
"""
import requests
import json
import sys

def check_server_status():
    """Check if the server is running and responding"""
    try:
        response = requests.post("http://localhost:8000/twilio/voice", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responding")
            print(f"   Status: {response.status_code}")
            if "Response" in response.text:
                print("   TwiML: Valid")
            else:
                print("   TwiML: Invalid")
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server on localhost:8000")
        return False
    except requests.exceptions.Timeout:
        print("❌ Server request timed out")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False

def check_ngrok_status():
    """Check if ngrok is running"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            data = response.json()
            tunnels = data.get('tunnels', [])
            if tunnels:
                print("✅ ngrok is running")
                for tunnel in tunnels:
                    if tunnel.get('proto') == 'https':
                        public_url = tunnel.get('public_url', '')
                        print(f"   Public URL: {public_url}")
                        return public_url
            else:
                print("⚠️  ngrok is running but no tunnels found")
                return None
        else:
            print("❌ ngrok API responded with error")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ ngrok not running (no response on localhost:4040)")
        return None
    except Exception as e:
        print(f"❌ Error checking ngrok: {e}")
        return None

def main():
    print("🎙️  Voice Assistant Status Check")
    print("=" * 40)
    
    # Check server
    server_ok = check_server_status()
    
    # Check ngrok
    ngrok_url = check_ngrok_status()
    
    print("\n📋 Summary:")
    if server_ok and ngrok_url:
        print("✅ System is ready!")
        print(f"   Configure Twilio webhook: {ngrok_url}/twilio/voice")
    elif server_ok:
        print("⚠️  Server is running but ngrok is not")
        print("   Start ngrok with: ngrok http 8000")
    elif ngrok_url:
        print("⚠️  ngrok is running but server is not")
        print("   Start server with: uvicorn router.pipeline:app --host 0.0.0.0 --port 8000")
    else:
        print("❌ Both server and ngrok need to be started")
        print("   1. Start server: uvicorn router.pipeline:app --host 0.0.0.0 --port 8000")
        print("   2. Start ngrok: ngrok http 8000")

if __name__ == "__main__":
    main() 