# src/ptt_voice_app.py
from pathlib import Path
from bridge import NLUBridge
from actions import handle_intent
from voice import STTEngine, tts_espeak
from gpio_ptt import PushToTalk

def main():
    project_root = Path(__file__).resolve().parents[1]
    nlu = NLUBridge(kb_path=project_root / "prolog" / "nlu.pl")

    # Ajusta 'device' si quieres forzar un mic en específico (usa el índice de sounddevice)
    stt = STTEngine(model_dir=str(project_root / "models" / "vosk-model-small-es"), device=None)
    ptt = PushToTalk(btn_pin=17, led_pin=27, hold_to_talk=True, exit_longpress_sec=3.0)

    print("Asistente (voz+PTT). Mantén presionado el botón para hablar. Long-press (~3s) para salir.")
    tts_espeak("Asistente listo. Mantén presionado el botón para hablar.")

    while True:
        try:
            mode = ptt.wait_for_trigger()
            if mode == "exit":
                tts_espeak("Cerrando. Hasta luego.")
                print("Saliendo por long-press del botón.")
                break

            with ptt.talk_guard():
                tts_espeak("Te escucho.")
                text = stt.listen_once(timeout_sec=8)  # ajusta si quieres más tiempo
            if not text:
                tts_espeak("No te escuché bien.")
                continue

            print(f"[Tú]: {text}")
            result = nlu.parse(text)
            intent = result["intent"]
            reply  = result["reply"]
            out = handle_intent(intent, reply)
            print(f"[Asistente]: {out}")
            tts_espeak(out)

        except KeyboardInterrupt:
            print("\nInterrumpido. Saliendo…")
            break

if __name__ == "__main__":
    main()
