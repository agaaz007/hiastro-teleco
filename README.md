# Convo-AI Exotel Voice Assistant – Local Setup Guide

## Overview
A real-time, phone-grade conversational voice agent for Exotel/Twilio, using FastAPI, OpenAI, and real-time audio streaming. This guide is for **local development without Docker** (using `uvicorn` or the provided Python script).

---

## 1. Prerequisites
- **Python 3.8+** (Recommended: 3.11+)
- **ngrok** (for webhook testing)
- **Twilio or Exotel account** (for phone integration)

---

## 2. Clone the Repository
```sh
git clone <your-repo-url>
cd convo-ai-exotel
```

---

## 3. Install Python Dependencies
From the project root:
```sh
pip install -r requirements.txt
```
Or, if you prefer Poetry (optional):
```sh
cd router
poetry install
```

---

## 4. Set Up Environment Variables
- Copy the sample env file and fill in your credentials:
  ```sh
  cp infra/env.sample .env
  ```
- Edit `.env` and provide values for:
  - `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`
  - `PLAYHT_USER_ID`, `PLAYHT_API_KEY`
  - `AZURE_TTS_KEY`
  - `OPENAI_API_KEY`
  - `REDIS_URL` (default is fine for local)

---

## 5. Start ngrok (for Webhook Testing)
Expose your local server to the internet:
```sh
ngrok http 8000
```
- Copy the HTTPS URL from ngrok (e.g., `https://abcd1234.ngrok.io`).

---

## 6. Start the FastAPI Server
From the project root or inside the `router/` directory, run:
```sh
python router/start_server.py
```
- This script will auto-detect your ngrok URL and start the server at `http://localhost:8000`.

**OR** run directly with uvicorn:
```sh
uvicorn router.pipeline:app --host 0.0.0.0 --port 8000 --reload
```

---

## 7. Configure Twilio/Exotel Webhook
- In your Twilio/Exotel console, set the webhook for your number to:
  - `wss://<ngrok-url>/ws/twilio`
  - or `https://<ngrok-url>/ws/twilio`
  (Use `https://` if `wss://` is not supported.)

---

## 8. Test the System
- Call your Twilio/Exotel number.
- You should hear a compliance announcement, then be able to converse with the AI in real time.

---

## 9. (Optional) Check System Status
```sh
python router/check_status.py
```

---

## 10. Troubleshooting
- Logs are written to the `logs/` directory.
- Check for missing environment variables or dependency errors.
- See `router/README.md` and `router/TROUBLESHOOTING.md` for more help.

---

## Notes
- You do **NOT** need Docker for this setup.
- Just install dependencies, set up your `.env`, start ngrok, and run the server with `python router/start_server.py` or `uvicorn`.
- Then point your Twilio/Exotel webhook to your ngrok URL.

---

**For any issues or advanced configuration, see the documentation in the `router/` folder.**
