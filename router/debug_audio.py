#!/usr/bin/env python3
"""
Audio Debugging Tool for Voice Assistant
"""
import asyncio
import websockets
import json
import time
import base64
import requests

async def test_websocket_connection():
    """Test WebSocket connection to the voice assistant"""
    uri = "ws://localhost:8000/ws/twilio"
    
    try:
        print("🔌 Testing WebSocket connection...")
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connected successfully!")
            
            # Send a test start message
            start_message = {
                "event": "start",
                "start": {
                    "streamSid": "test-stream-123",
                    "accountSid": "test-account",
                    "callSid": "test-call"
                }
            }
            
            await websocket.send(json.dumps(start_message))
            print("📤 Sent start message")
            
            # Wait for any responses
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"📥 Received: {response}")
            except asyncio.TimeoutError:
                print("⏰ No immediate response (this might be normal)")
            
            # Send a test media message (silence)
            silence_payload = base64.b64encode(b'\xFF' * 160).decode()
            media_message = {
                "event": "media",
                "media": {
                    "payload": silence_payload
                }
            }
            
            await websocket.send(json.dumps(media_message))
            print("📤 Sent test audio data")
            
            # Wait for responses
            print("👂 Listening for responses...")
            for i in range(10):
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                    print(f"📥 Response {i+1}: {response[:100]}...")
                except asyncio.TimeoutError:
                    print(f"⏰ Timeout {i+1}/10")
                    break
                    
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")
        return False
    
    return True

def test_twilio_webhook():
    """Test the Twilio webhook endpoint"""
    print("\n📞 Testing Twilio webhook...")
    
    try:
        response = requests.post("http://localhost:8000/twilio/voice", timeout=5)
        if response.status_code == 200:
            print("✅ Webhook responding correctly")
            twiml = response.text
            
            # Check TwiML content
            if "Stream url=" in twiml:
                print("✅ TwiML contains Stream directive")
                # Extract the URL
                import re
                url_match = re.search(r'url="([^"]+)"', twiml)
                if url_match:
                    stream_url = url_match.group(1)
                    print(f"📡 Stream URL: {stream_url}")
                    
                    # Check if it's the correct protocol
                    if stream_url.startswith("wss://"):
                        print("✅ Using secure WebSocket (wss://)")
                    else:
                        print("⚠️  Not using secure WebSocket - should be wss://")
                else:
                    print("❌ Could not extract stream URL")
            else:
                print("❌ TwiML missing Stream directive")
                
            print(f"📄 TwiML Response:\n{twiml}")
            
        else:
            print(f"❌ Webhook returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")
        return False
    
    return True

def check_ngrok_status():
    """Check ngrok status and tunnels"""
    print("\n🌐 Checking ngrok status...")
    
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            data = response.json()
            tunnels = data.get('tunnels', [])
            
            if tunnels:
                print("✅ ngrok is running with tunnels:")
                for tunnel in tunnels:
                    proto = tunnel.get('proto', 'unknown')
                    public_url = tunnel.get('public_url', 'unknown')
                    local_addr = tunnel.get('config', {}).get('addr', 'unknown')
                    print(f"  📡 {proto}: {public_url} → {local_addr}")
                    
                    if proto == 'https':
                        wss_url = public_url.replace('https://', 'wss://')
                        print(f"  🔗 WebSocket URL: {wss_url}/ws/twilio")
                return True
            else:
                print("⚠️  ngrok running but no tunnels found")
                return False
        else:
            print(f"❌ ngrok API returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Cannot connect to ngrok: {e}")
        print("💡 Make sure ngrok is running: ngrok http 8000")
        return False

async def main():
    """Run all diagnostic tests"""
    print("🎙️  Voice Assistant Audio Diagnostic Tool")
    print("=" * 50)
    
    # Test 1: Check ngrok
    ngrok_ok = check_ngrok_status()
    
    # Test 2: Check Twilio webhook
    webhook_ok = test_twilio_webhook()
    
    # Test 3: Check WebSocket connection
    websocket_ok = await test_websocket_connection()
    
    # Summary
    print("\n📋 Diagnostic Summary:")
    print("=" * 30)
    print(f"🌐 ngrok: {'✅ OK' if ngrok_ok else '❌ ISSUE'}")
    print(f"📞 Webhook: {'✅ OK' if webhook_ok else '❌ ISSUE'}")
    print(f"🔌 WebSocket: {'✅ OK' if websocket_ok else '❌ ISSUE'}")
    
    if all([ngrok_ok, webhook_ok, websocket_ok]):
        print("\n🎉 All tests passed! The issue might be:")
        print("   1. Twilio phone number webhook configuration")
        print("   2. OpenAI API key or model access")
        print("   3. Audio codec issues on the phone/carrier side")
        print("\n💡 Next steps:")
        print("   1. Check Twilio Console webhook configuration")
        print("   2. Make a test call and check server logs")
        print("   3. Verify OpenAI API key has Realtime API access")
    else:
        print("\n⚠️  Issues detected! Fix the failed tests above.")

if __name__ == "__main__":
    asyncio.run(main()) 