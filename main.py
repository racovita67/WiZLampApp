from wiz_lamp_gui import App_GUI
from wiz_lamp_gui import map_valrange
from lamp import WiZLampUDS
import json
import os

class Controller:
    script_dn = os.path.dirname(os.path.abspath(__file__))
    json_fn = os.path.join(script_dn, "data.json")
    def __init__(self):
        # Controller Data

        self.lamp_on_off_flag = False
        self.lamp_intensity = 50
        self.lamp_hot_cold = 50
        # Model and View
        self.model = WiZLampUDS()
        self.model.search_ip()  # Search for lamp's ip
        self.view = App_GUI()
        self.view.main_frame.slider_intensity.configure(command=self.slider_event_intensity)
        self.view.main_frame.slider_warm_cold.configure(command=self.slider_event_hot_cold)
        self.view.main_frame.btn_on_off.configure(command=self.btn_on_off)
        self.view.main_frame.btn_sendintensity.configure(command=self.btn_set_intensity)
        self.view.main_frame.btn_sendgradient.configure(command=self.btn_set_hot_cold)

    def slider_event_intensity(self, value):
        self.view.main_frame.intensity_event(value)
        self.lamp_intensity = int(value)

    def slider_event_hot_cold(self, value):
        self.view.main_frame.cold_hot_event(value)
        self.lamp_hot_cold = int(value)
    
    def btn_on_off(self):
        if self.lamp_on_off_flag == True:
            self.model.send_uds_command({"state": True})
            self.lamp_on_off_flag = False
        else:
            self.model.send_uds_command({"state": False})
            self.lamp_on_off_flag = True
            
    def btn_set_intensity(self):
        self.model.send_uds_command({"dimming": int(self.lamp_intensity)})

    def btn_set_hot_cold(self):
        with open(self.json_fn) as f:
            hot_map = json.load(f)["hot_cold_map"]

        hm_idx = int(map_valrange(self.lamp_hot_cold, (0, 100), (0, (len(hot_map) - 40))))
        color = hot_map[hm_idx]["hex"]
        params = {
                "r": int("0x"+color[1:3], 16),
                "g": int("0x"+color[3:5], 16),
                "b": int("0x"+color[5:7], 16),
                "transition": 100  # transition time in deciseconds (0 = instant)
            }
        self.model.send_uds_command(params)
    
if __name__ == "__main__":
    # Get screen resolution
    c = Controller()
    c.view.mainloop()