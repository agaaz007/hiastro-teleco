# 🔧 Voice Assistant Troubleshooting Guide

## 🎵 "I Cannot Hear Any Audio" Issue

### Quick Diagnosis

Run the diagnostic tool first:
```bash
python debug_audio.py
```

If all tests pass ✅, the issue is likely in the Twilio configuration.

### 🔍 Step-by-Step Troubleshooting

#### 1. **Check Twilio Phone Number Configuration**

**This is the most common cause of no audio!**

1. Go to [Twilio Console](https://console.twilio.com/)
2. Navigate to **Phone Numbers** → **Manage** → **Active Numbers**
3. Click on your phone number
4. In the **"Voice"** section, verify:
   - **Webhook URL**: `https://YOUR-NGROK-URL.ngrok-free.app/twilio/voice`
   - **HTTP Method**: `POST`
   - **Status**: Should be green/active

**Get your current ngrok URL:**
```bash
python check_status.py
```

#### 2. **Verify Server is Running**

```bash
ps aux | grep uvicorn
```

If not running, start it:
```bash
cd /Users/Agaaz/convo-ai
export NGROK_URL="wss://YOUR-NGROK-URL.ngrok-free.app"
uvicorn router.pipeline:app --host 0.0.0.0 --port 8000
```

#### 3. **Check ngrok Status**

```bash
curl -s localhost:4040/api/tunnels | jq '.tunnels[0].public_url'
```

If ngrok is not running:
```bash
ngrok http 8000
```

#### 4. **Test WebSocket Connection**

```bash
python debug_audio.py
```

Look for the WebSocket test results.

#### 5. **Monitor Real-time Activity**

When making a test call, monitor the server logs:
```bash
python monitor_logs.py
```

Then make a call to your Twilio number.

### 📋 Common Issues and Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Wrong webhook URL** | No server logs when calling | Update Twilio webhook URL |
| **ngrok tunnel expired** | Webhook returns 404 | Restart ngrok, update webhook |
| **Server not running** | Connection refused | Start uvicorn server |
| **OpenAI API issues** | WebSocket connects but no AI response | Check API key and model access |
| **Audio codec issues** | AI responds but no audio heard | Check phone/carrier compatibility |

### 🎯 Expected Behavior

When working correctly, you should see:

1. **Webhook Call**: Server logs show POST to `/twilio/voice`
2. **WebSocket Connection**: `[DEBUG] WebSocket connection established`
3. **Audio Processing**: `[AUDIO] Sending X bytes to OpenAI`
4. **AI Response**: `[TRANSCRIPT] AI response text`
5. **Audio Output**: `[TWILIO OUT] Sending audio frames`

### 🔧 Advanced Debugging

#### Enable Verbose Logging

Add this to your server startup:
```bash
export PYTHONPATH=/Users/Agaaz/convo-ai
uvicorn router.pipeline:app --host 0.0.0.0 --port 8000 --log-level debug
```

#### Test Audio Pipeline

Test the test tone feature:
```python
# The server automatically sends a test tone when a call starts
# You should hear a 440Hz tone for 2 seconds
```

#### Check OpenAI API Access

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     -H "OpenAI-Beta: realtime=v1" \
     "https://api.openai.com/v1/models" | grep realtime
```

### 🆘 Still No Audio?

If you've checked everything above and still have no audio:

1. **Phone/Carrier Issues**: Try calling from a different phone or carrier
2. **Twilio Account Issues**: Check your Twilio account balance and status
3. **OpenAI Rate Limits**: Check if you're hitting API limits
4. **Network Issues**: Try restarting ngrok and the server

### 📞 Test Call Checklist

Before making a test call, verify:

- [ ] Server is running on port 8000
- [ ] ngrok is tunneling port 8000
- [ ] Twilio webhook URL is correct
- [ ] OpenAI API key is valid
- [ ] You can hear the initial "This call may be recorded..." message

### 💡 Pro Tips

1. **Use the diagnostic tool** before troubleshooting manually
2. **Check server logs** during test calls
3. **Test with different phones** to rule out device issues
4. **Monitor ngrok logs** for webhook calls
5. **Verify OpenAI model access** in the API playground

### 🎉 Success Indicators

You'll know it's working when:
- You hear the initial TwiML message
- You hear the 440Hz test tone
- The AI responds to your speech
- You can have a conversation with the AI 