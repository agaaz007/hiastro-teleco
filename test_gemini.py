#!/usr/bin/env python3
"""
Simple test script to verify Gemini Live API setup
"""
import os
import asyncio
import sys
from google import genai
from google.genai import types
import numpy as np

# Compatibility for Python < 3.11
if sys.version_info < (3, 11, 0):
    try:
        import taskgroup
        asyncio.TaskGroup = taskgroup.TaskGroup
    except ImportError:
        print("❌ TaskGroup not available. Please upgrade to Python 3.11+ or install taskgroup: pip install taskgroup")
        sys.exit(1)

async def test_gemini_connection():
    """Test basic Gemini Live API connection"""
    try:
        client = genai.Client(http_options={"api_version": "v1alpha"})
        model = "gemini-2.5-flash-preview-native-audio-dialog"
        config = types.LiveConnectConfig(
            response_modalities=["AUDIO"],
            proactivity={'proactive_audio': True},
        )
        
        print("🤖 Testing Gemini Live API connection...")
        
        async with client.aio.live.connect(model=model, config=config) as session:
            print("✅ Connected to Gemini Live API successfully!")
            
            # Generate a simple test audio (1 second of silence at 16kHz)
            sample_rate = 16000
            duration = 1.0
            samples = int(sample_rate * duration)
            test_audio = np.zeros(samples, dtype=np.int16)
            
            print("🎤 Sending test audio...")
            await session.send_realtime_input(
                audio=types.Blob(data=test_audio.tobytes(), mime_type="audio/pcm;rate=16000")
            )
            
            print("👂 Listening for response...")
            response_count = 0
            turn = session.receive()
            async for response in turn:
                response_count += 1
                print(f"📦 Response {response_count}: {type(response)}")
                if response.data is not None:
                    print(f"🔊 Received audio response: {len(response.data)} bytes")
                    break
                if response.text:
                    print(f"📝 Received text: {response.text}")
                if response_count > 10:  # Timeout after 10 responses
                    break
            
            print("✅ Test completed successfully!")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY environment variable not set!")
        print("Please set it with: export GOOGLE_API_KEY='your-api-key-here'")
        exit(1)
    
    asyncio.run(test_gemini_connection()) 