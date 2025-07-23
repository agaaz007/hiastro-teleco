import audioop
import numpy as np
from scipy.signal import resample

def ulaw8k_to_pcm16k(ulaw_bytes):
    """Convert μ-law 8kHz audio to PCM 16kHz for Gemini"""
    try:
        # μ-law (8kHz) to PCM (8kHz)
        pcm_8k = audioop.ulaw2lin(ulaw_bytes, 2)
        pcm_np = np.frombuffer(pcm_8k, dtype=np.int16)
        # Resample to 16kHz (double the sample rate)
        pcm_16k = resample(pcm_np, len(pcm_np) * 2)
        # Ensure proper data type and range
        pcm_16k = np.clip(pcm_16k, -32767, 32767).astype(np.int16)
        return pcm_16k.tobytes()
    except Exception as e:
        print(f"❌ Error in ulaw8k_to_pcm16k: {e}")
        return b""

def pcm24k_to_ulaw8k(pcm24k_bytes):
    """Convert PCM 24kHz audio from Gemini to μ-law 8kHz for Twilio"""
    try:
        # PCM 24kHz to numpy array
        pcm24k_np = np.frombuffer(pcm24k_bytes, dtype=np.int16)
        # Resample to 8kHz (divide by 3)
        pcm8k_np = resample(pcm24k_np, len(pcm24k_np) // 3)
        # Ensure proper data type and range
        pcm8k_np = np.clip(pcm8k_np, -32767, 32767).astype(np.int16)
        # Convert to bytes
        pcm8k_bytes = pcm8k_np.tobytes()
        # PCM (8kHz) to μ-law
        ulaw_bytes = audioop.lin2ulaw(pcm8k_bytes, 2)
        return ulaw_bytes
    except Exception as e:
        print(f"❌ Error in pcm24k_to_ulaw8k: {e}")
        return b"" 