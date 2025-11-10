# src/voice.py
import queue, sys, json, subprocess, time
from pathlib import Path
import sounddevice as sd
import soundfile as sf
from vosk import Model, KaldiRecognizer
import numpy as np

TARGET_SR = 16000   # Vosk ideal
CHANNELS  = 1
BLOCK_DUR = 0.05
SILENCE_SEC = 0.8
ENERGY_THRESH = 0.002

def resample_linear_int16(buf_bytes: bytes, in_sr: int, out_sr: int) -> bytes:
    """Re-muestreo lineal simple (suficiente para STT)."""
    if in_sr == out_sr:
        return buf_bytes
    x = np.frombuffer(buf_bytes, dtype=np.int16).astype(np.float32)
    n = len(x)
    if n == 0:
        return b""
    t_old = np.linspace(0, 1, num=n, endpoint=False)
    new_n = int(round(n * (out_sr / in_sr)))
    if new_n <= 0:
        return b""
    t_new = np.linspace(0, 1, num=new_n, endpoint=False)
    y = np.interp(t_new, t_old, x).astype(np.int16)
    return y.tobytes()

class STTEngine:
    def __init__(self, model_dir="models/vosk-model-small-es", device=None):
        model_path = Path(model_dir)
        if not model_path.exists():
            raise RuntimeError(f"No encuentro el modelo Vosk en {model_path}.")

        # Descubrir samplerate del dispositivo de entrada
        self.device = device
        dev_info = sd.query_devices(device, "input")
        self.in_sr = int(dev_info.get("default_samplerate") or 16000)
        if self.in_sr <= 0:
            self.in_sr = 16000  # fallback

        self.model = Model(str(model_path))
        self.rec = KaldiRecognizer(self.model, TARGET_SR)
        self.rec.SetWords(True)

    def listen_once(self, device=None, timeout_sec=8):
        q = queue.Queue()

        def audio_cb(indata, frames, time_, status):
            if status:
                print(status, file=sys.stderr)
            q.put(bytes(indata))

        with sd.RawInputStream(
            samplerate=self.in_sr,
            blocksize=int(self.in_sr * BLOCK_DUR),
            dtype="int16",
            channels=CHANNELS,
            callback=audio_cb,
            device=(device if device is not None else self.device),
        ):
            last_voice = time.time()
            self.rec.Reset()

            while True:
                try:
                    data = q.get(timeout=timeout_sec)
                except queue.Empty:
                    break

                # energía para silencio
                arr = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
                energy = float(np.mean(arr**2))
                if energy > ENERGY_THRESH:
                    last_voice = time.time()

                # re-muestrear si hace falta
                if self.in_sr != TARGET_SR:
                    data_for_vosk = resample_linear_int16(data, self.in_sr, TARGET_SR)
                else:
                    data_for_vosk = data

                if self.rec.AcceptWaveform(data_for_vosk):
                    pass  # no usamos parciales aquí

                if time.time() - last_voice > SILENCE_SEC:
                    break

            try:
                result = json.loads(self.rec.FinalResult())
                text = (result.get("text") or "").strip().lower()
            except Exception:
                text = ""

        return text

def tts_espeak(text: str, voice="es", speed_wpm=170):
    if not text:
        return
    subprocess.run(["espeak-ng", "-v", voice, "-s", str(speed_wpm), text])

def save_wav(filename: str, data: np.ndarray):
    sf.write(filename, data, TARGET_SR)
