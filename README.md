
<<<<<<< HEAD
# hiastro-teleco
hiastro-teleco
=======
# Convo-AI: Real-Time Conversational Voice Agent

## Overview
A cloud-native, phone-grade conversational voice agent supporting real-time barge-in, natural overlap, and low-latency operation. Integrates Twilio PSTN, Pipecat, faster-whisper, LangChain, PlayHT/Azure TTS, Redis, and Grafana. Designed for compliance (TRAI), reliability, and developer velocity.

## Architecture
- **router/**: Pipecat pipeline (VAD, ASR, Agent, TTS), FastAPI WebSocket server
- **asr/**: GPU-accelerated faster-whisper-server
- **agent/**: LangChain agent, tool orchestration
- **infra/**: Terraform, Docker Compose, CI/CD, monitoring

## Key Features
- Real-time barge-in (interrupt TTS mid-utterance)
- <800ms mouth-to-ear latency (p95)
- Dual-channel recording, 90-day S3 retention (TRAI)
- Observability: Prometheus, RedisTimeSeries, Grafana
- Blue-green deploy, GPU autoscaling

## Quickstart
1. Clone repo, set up `.env` (see infra/env.sample)
2. `docker compose up --build` (GPU required for ASR)
3. Configure Twilio number to point to router WS endpoint
4. Access Grafana dashboard at :3000 (default)

## Directory Structure
- `router/` – Pipecat pipeline, FastAPI, TTS/ASR integration
- `asr/` – faster-whisper-server (GPU)
- `agent/` – LangChain agent, tools
- `infra/` – Terraform, Docker Compose, CI/CD, monitoring

## Compliance
- TRAI: 90-day dual-channel recording, announcement
- PCI-DSS: No card data stored, HTTPS everywhere

## Contact
See PRD for stakeholders and escalation paths.

## Local Testing with ngrok

To test Twilio calls locally:
1. Start your router service (FastAPI) on port 443 or 8000.
2. Run ngrok to expose your local port:
   
   ```sh
   ngrok http 443
   # or if using port 8000:
   ngrok http 8000
   ```
3. Copy the HTTPS URL from ngrok (e.g., `https://abcd1234.ngrok.io`).
4. In the Twilio Console, set the Voice webhook for your number to:
   
   ```
   wss://<ngrok-url>/ws/twilio
   ```
   (Use `https://` if Twilio does not support `wss://` directly; your FastAPI should accept both.)

5. Call your Twilio number to test the integration. 
>>>>>>> 6c4ed91 (Initial commit: Add full codebase)
>>>>>>> 7d320eb (Initial commit: Add full codebase)
