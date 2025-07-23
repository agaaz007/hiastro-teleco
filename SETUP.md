# Gemini Live API + Twilio Voice Assistant Setup

## Prerequisites

1. **Google API Key**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **Twilio Account**: For phone number and voice streaming
3. **ngrok**: For exposing local server to the internet

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   ```bash
   export GOOGLE_API_KEY="your-google-api-key-here"
   export NGROK_URL="wss://your-ngrok-subdomain.ngrok-free.app"
   export BACKGROUND_NOISE_VOLUME="0.05"  # Optional: Background noise level (0.0-0.2)
   ```

3. **Test Gemini connection**:
   ```bash
   python test_gemini.py
   ```

4. **Test background noise** (optional):
   ```bash
   python test_background_noise.py
   ```
   This creates a sample WAV file you can listen to.