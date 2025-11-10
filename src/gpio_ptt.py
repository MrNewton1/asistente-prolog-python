# src/gpio_ptt.py
from gpiozero import Button, LED
from time import monotonic, sleep

class PushToTalk:
    """
    Botón en GPIO17 para iniciar la escucha
    LED en GPIO27 para indicar "escuchando"
    """
    def __init__(self, btn_pin=17, led_pin=27, hold_to_talk=True, exit_longpress_sec=3.0):
        self.button = Button(btn_pin, pull_up=True, bounce_time=0.03)
        self.led = None
        self.exit_longpress_sec = exit_longpress_sec
        self.hold_to_talk = hold_to_talk  # True: escucha mientras esté presionado

        try:
            self.led = LED(led_pin)  # opcional
        except Exception:
            self.led = None

    def _led_on(self):
        if self.led:
            self.led.on()

    def _led_off(self):
        if self.led:
            self.led.off()

    def wait_for_trigger(self):
        """
        Bloquea hasta que detecta una pulsación "válida".
        Si se mantiene presionado > exit_longpress_sec, devuelve 'exit'.
        Devuelve 'talk' cuando debe iniciar escucha.
        """
        self.button.wait_for_press()
        t0 = monotonic()

        # Detectar long-press para salir
        while self.button.is_pressed:
            if monotonic() - t0 >= self.exit_longpress_sec:
                return "exit"
            sleep(0.02)

        # Si no fue long-press, es un "tap" (o press corto)
        return "talk"

    def talk_guard(self):
        """
        Context manager: enciende LED al empezar a escuchar y lo apaga al terminar.
        """
        class _Ctx:
            def __init__(self, outer): self.outer = outer
            def __enter__(self): self.outer._led_on()
            def __exit__(self, *exc): self.outer._led_off()
        return _Ctx(self)
