#!/usr/bin/env python3
"""
Test script to simulate audio flow and identify where frames are lost
"""
import asyncio
import websockets
import json
import base64
import time

async def test_audio_flow():
    """Test the complete audio pipeline"""
    print("🧪 Testing Audio Flow Pipeline")
    print("=" * 40)
    
    uri = "ws://localhost:8000/ws/twilio"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to debug server")
            
            # Step 1: Send start message (simulates Twilio starting a call)
            start_message = {
                "event": "start",
                "start": {
                    "streamSid": "test-stream-audio-debug",
                    "accountSid": "test-account",
                    "callSid": "test-call-audio-debug"
                }
            }
            
            await websocket.send(json.dumps(start_message))
            print("📤 Sent start message - should trigger test tone")
            
            # Step 2: Listen for audio frames coming back
            print("👂 Listening for audio frames from server...")
            frame_count = 0
            
            for i in range(20):  # Listen for 20 messages
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                    msg = json.loads(response)
                    
                    if msg.get("event") == "media":
                        frame_count += 1
                        payload = msg.get("media", {}).get("payload", "")
                        print(f"📥 Received audio frame #{frame_count}: {payload[:16]}...")
                        
                        # Decode and check frame
                        try:
                            audio_data = base64.b64decode(payload)
                            print(f"   📊 Frame size: {len(audio_data)} bytes")
                            
                            # Check if it's silence or actual audio
                            if len(set(audio_data)) == 1:
                                print("   🔇 Frame contains silence")
                            else:
                                print("   🎵 Frame contains audio data")
                                
                        except Exception as e:
                            print(f"   ❌ Error decoding frame: {e}")
                            
                    elif msg.get("event") == "mark":
                        mark_name = msg.get("mark", {}).get("name", "unknown")
                        print(f"📍 Received mark: {mark_name}")
                        
                    else:
                        print(f"📨 Other message: {msg.get('event', 'unknown')}")
                        
                except asyncio.TimeoutError:
                    print(f"⏰ Timeout {i+1}/20 - no message received")
                    
            print(f"\n📊 Test Results:")
            print(f"   🎵 Audio frames received: {frame_count}")
            
            if frame_count > 0:
                print("   ✅ Audio frames are being sent from server to client")
                print("   💡 If you can't hear audio, the issue is likely:")
                print("      1. Twilio webhook not configured correctly")
                print("      2. Real phone call not connecting to WebSocket")
                print("      3. Audio codec issues on phone/carrier side")
            else:
                print("   ❌ No audio frames received - pipeline issue detected")
                print("   🔧 Check server logs for audio generation problems")
                
            # Step 3: Send some test audio to trigger AI response
            print("\n🎤 Sending test audio to trigger AI response...")
            silence_payload = base64.b64encode(b'\xFF' * 160).decode()
            
            for i in range(5):
                media_message = {
                    "event": "media",
                    "media": {
                        "payload": silence_payload
                    }
                }
                await websocket.send(json.dumps(media_message))
                
            print("📤 Sent 5 audio frames to server")
            
            # Listen for AI response
            print("👂 Listening for AI response...")
            ai_frames = 0
            
            for i in range(30):  # Listen for 30 seconds
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    msg = json.loads(response)
                    
                    if msg.get("event") == "media":
                        ai_frames += 1
                        payload = msg.get("media", {}).get("payload", "")
                        print(f"📥 AI response frame #{ai_frames}: {payload[:16]}...")
                        
                except asyncio.TimeoutError:
                    if i > 10:  # Give AI time to respond
                        break
                    continue
                    
            print(f"\n📊 AI Response Test:")
            print(f"   🤖 AI audio frames received: {ai_frames}")
            
            if ai_frames > 0:
                print("   ✅ AI is generating audio responses")
            else:
                print("   ❌ AI not generating audio - check OpenAI connection")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
        
    return True

async def main():
    print("🔧 Audio Pipeline Test")
    print("Make sure the debug server is running first!")
    print()
    
    success = await test_audio_flow()
    
    if success:
        print("\n🎉 Test completed successfully!")
        print("Check the debug server logs for detailed pipeline information.")
    else:
        print("\n❌ Test failed - check debug server logs for errors.")

if __name__ == "__main__":
    asyncio.run(main()) 