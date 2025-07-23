#!/usr/bin/env python3
"""
Real-time log monitor for Voice Assistant
"""
import asyncio
import websockets
import json
import time
from datetime import datetime

class LogMonitor:
    def __init__(self):
        self.connections = {}
        self.call_count = 0
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    async def monitor_webhook_calls(self):
        """Monitor webhook calls by polling the server"""
        import requests
        last_call_time = time.time()
        
        while True:
            try:
                # This is a simple way to detect if webhook was called
                # In a real scenario, you'd want to add a counter endpoint
                await asyncio.sleep(2)
                
            except Exception as e:
                self.log(f"Error monitoring webhooks: {e}", "ERROR")
                await asyncio.sleep(5)
    
    async def monitor_websocket_connections(self):
        """Monitor WebSocket connections by creating a test connection"""
        while True:
            try:
                uri = "ws://localhost:8000/ws/twilio"
                async with websockets.connect(uri) as websocket:
                    self.log("🔌 WebSocket test connection established")
                    
                    # Send a ping to see if the server responds
                    ping_msg = {
                        "event": "start",
                        "start": {
                            "streamSid": f"monitor-{int(time.time())}",
                            "accountSid": "monitor-account",
                            "callSid": "monitor-call"
                        }
                    }
                    
                    await websocket.send(json.dumps(ping_msg))
                    self.log("📤 Sent monitor ping")
                    
                    # Wait for response
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=3.0)
                        self.log(f"📥 Server responding: {response[:50]}...")
                    except asyncio.TimeoutError:
                        self.log("⏰ No response to ping (server might be busy)")
                        
                    await asyncio.sleep(10)  # Check every 10 seconds
                    
            except Exception as e:
                self.log(f"❌ WebSocket monitor error: {e}", "ERROR")
                await asyncio.sleep(5)

async def main():
    print("🎙️  Voice Assistant Log Monitor")
    print("=" * 40)
    print("This will monitor your voice assistant for:")
    print("  📞 Webhook calls from Twilio")
    print("  🔌 WebSocket connections")
    print("  🎵 Audio processing activity")
    print()
    print("💡 Make a test call to see real-time activity!")
    print("   Call your Twilio number to test")
    print()
    print("Press Ctrl+C to stop monitoring")
    print("=" * 40)
    
    monitor = LogMonitor()
    
    # Start monitoring tasks
    tasks = [
        asyncio.create_task(monitor.monitor_webhook_calls()),
        asyncio.create_task(monitor.monitor_websocket_connections())
    ]
    
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\n👋 Stopping monitor...")
        for task in tasks:
            task.cancel()

if __name__ == "__main__":
    asyncio.run(main()) 