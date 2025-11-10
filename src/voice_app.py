# src/voice_app.py
from bridge import NLUBridge
from actions import handle_intent
from voice import STTEngine, tts_espeak

def main():
    nlu = NLUBridge()
    stt = STTEngine(model_dir="models/vosk-model-small-es")

    print("Asistente (voz). Pulsa Enter para hablar. Ctrl+C para salir.")
    while True:
        try:
            inp = input("[Enter=hablar / 'q'=salir] > ").strip().lower()
            if inp == "q":
                break

            tts_espeak("Te escucho.")
            text = stt.listen_once(timeout_sec=8)
            if not text:
                tts_espeak("No te escuché bien. Intenta de nuevo.")
                continue

            print(f"[Tú]: {text}")
            result = nlu.parse(text)
            intent = result["intent"]
            reply  = result["reply"]
            out = handle_intent(intent, reply)
            print(f"[Asistente]: {out}")
            tts_espeak(out)

        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo… ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
