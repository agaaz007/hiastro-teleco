#!/usr/bin/env python3
"""
Run the audio debugging server
"""
import os
import subprocess
import sys

def main():
    print("🔧 Starting Audio Debug Server")
    print("=" * 50)
    
    # Set environment variables
    os.environ["NGROK_URL"] = "wss://71b7-2401-4900-1c8a-a014-5b7-2683-cb54-74fb.ngrok-free.app"
    
    print(f"📡 Using ngrok URL: {os.environ['NGROK_URL']}")
    print()
    print("🎯 This debug server will show you:")
    print("   📞 When Twilio calls the webhook")
    print("   🔌 WebSocket connection status")
    print("   🎵 Audio received from OpenAI")
    print("   🔧 Audio frames generated")
    print("   📤 Frames queued for Twilio")
    print("   📡 Frames sent to Twilio")
    print("   📊 Summary statistics every 10 seconds")
    print()
    print("💡 Make a test call to see detailed audio flow!")
    print("=" * 50)
    
    # Change to parent directory and run the debug server
    os.chdir("/Users/Agaaz/convo-ai")
    
    try:
        # Run the debug server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "router.audio_debug:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Debug server stopped")
    except Exception as e:
        print(f"❌ Error running debug server: {e}")

if __name__ == "__main__":
    main() 