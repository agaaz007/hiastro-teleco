# 🎙️ Twilio + OpenAI Realtime Voice Assistant

A real-time, phone-grade conversational voice agent using Twilio, OpenAI Realtime API, and FastAPI.

## Features

- 📞 **Phone Integration**: Call through Twilio phone numbers
- 🗣️ **Speech-to-Speech**: Direct audio conversation with AI
- 🚀 **Real-time**: Low-latency voice interaction
- 🎯 **Production Ready**: Proper error handling and logging
- 🔧 **Configurable**: Easy setup and customization

## Architecture

```
Caller → Twilio → WebSocket → FastAPI → OpenAI Realtime API
                                    ↓
Caller ← Twilio ← WebSocket ← FastAPI ← OpenAI Realtime API
```

## Setup

### 1. Install Dependencies

```bash
pip install fastapi uvicorn websocket-client numpy scipy audioop
```

### 2. Set Up Environment Variables

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-openai-api-key"

# Set your ngrok URL (optional - will auto-detect)
export NGROK_URL="wss://your-ngrok-url.ngrok-free.app"
```

### 3. Start ngrok

```bash
ngrok http 8000
```

### 4. Start the Server

**Option A: Using the helper script (recommended)**
```bash
cd router
python start_server.py
```

**Option B: Manual start**
```bash
uvicorn router.pipeline:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Configure Twilio

1. Go to your Twilio Console
2. Configure your phone number's webhook URL to: `http://your-ngrok-url.ngrok-free.app/twilio/voice`
3. Set HTTP method to `POST`

## Usage

1. Call your Twilio phone number
2. You'll hear: "This call may be recorded for compliance and quality assurance."
3. Start speaking - the AI will respond in real-time!

## Configuration

### Audio Settings
- **Format**: μ-law (G.711) at 8kHz
- **Frame Size**: 160 bytes (20ms)
- **Buffer Size**: 800-8000 bytes (100ms-1s)

### OpenAI Settings
- **Model**: `gpt-4o-realtime-preview-2025-06-03`
- **Voice**: `echo`
- **Modalities**: `audio` and `text`

## Troubleshooting

### Common Issues

1. **"Error loading ASGI app"**
   - Make sure you're in the correct directory
   - Use `uvicorn router.pipeline:app` from the project root

2. **"input_audio_buffer_commit_empty"**
   - This is normal - the system now filters out small audio chunks
   - The error indicates proper audio buffering is working

3. **No audio output**
   - Check ngrok URL is correct in TwiML
   - Verify OpenAI API key has Realtime API access
   - Check server logs for WebSocket connection issues

4. **Audio quality issues**
   - Ensure stable internet connection
   - Check for proper μ-law audio encoding
   - Verify Twilio webhook configuration

### Logs

The system provides detailed logging:
- `[TWILIO EVENT]` - Twilio WebSocket events
- `[OPENAI EVENT]` - OpenAI API events  
- `[AUDIO]` - Audio processing events
- `[DEBUG]` - General debug information
- `[ERROR]` - Error conditions

## API Endpoints

- `POST /twilio/voice` - Twilio voice webhook (returns TwiML)
- `WS /ws/twilio` - WebSocket for audio streaming

## Development

### Testing Audio

The system includes a test tone feature that plays a 440Hz sine wave when a call starts. This helps verify the audio pipeline is working correctly.

### Modifying AI Behavior

Edit the `instructions` in the session configuration:

```python
"instructions": "You are a helpful, witty, and friendly AI. Always respond in English, regardless of the user's language."
```

### Audio Processing

The system handles:
- Audio format conversion (μ-law ↔ PCM)
- Audio buffering and chunking
- Volume amplification (3x boost)
- Frame timing and synchronization

## Performance

- **Latency**: ~200-500ms end-to-end
- **Audio Quality**: Phone-grade (8kHz)
- **Concurrent Calls**: Limited by server resources
- **Reliability**: Production-ready with error handling

## License

MIT License - see LICENSE file for details. 