import time
import random
from threading import Thread

class AutoclickerController:
    def __init__(self, hardware):
        self.hardware = hardware

        self.min_cps = 5
        self.max_cps = 13
        self.pauses_enabled = False
        self.pause_intensity = 1

        self.clicker_enabled = False
        self.running = True
        self.session_clicks = 0

    def start(self):
        self.thread = Thread(target=self._input_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _input_loop(self):
        while self.running:
            if self.hardware.is_action_pressed("QUIT"):
                self.running = False
                break

            if self.hardware.is_action_pressed("TOGGLE"):
                self.clicker_enabled = not self.clicker_enabled
                while self.hardware.is_action_pressed("TOGGLE"):
                    time.sleep(0.01)

            if self.clicker_enabled and self.hardware.is_action_pressed("TRIGGER"):
                drop_chance = self.pause_intensity * 0.03

                if not self.pauses_enabled or random.random() > drop_chance:
                    target_cps = random.uniform(self.min_cps, self.max_cps)
                    target_total_delay = 1.0 / target_cps

                    hardware_delay = 0.015
                    remaining_delay = max(0.002, target_total_delay - hardware_delay)

                    split_ratio = random.uniform(0.3, 0.7)
                    down_delay = remaining_delay * split_ratio
                    up_delay = remaining_delay * (1.0 - split_ratio)

                    time.sleep(down_delay)
                    self.hardware.mouse_left_down()
                    time.sleep(hardware_delay)
                    time.sleep(up_delay)
                    self.hardware.mouse_left_up()

                    self.session_clicks += 1
                else:
                    time.sleep(random.uniform(0.08, 0.15))

            time.sleep(0.005) # minimise CPU usage
