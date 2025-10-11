import customtkinter
import tkinter
import json
from PIL import Image

def map_valrange(x_val, x_range: tuple, y_range: tuple):
    """
    Formula for modifying range:
    x in [a,b]. We want x to be in [c,d]

    Normalized x: x_n = (x - a)/(b - a) in [0,1]
    y = x_n * (d-c) + c
    """
    x_min = x_range[0]
    x_max = x_range[1]
    y_min = y_range[0]
    y_max = y_range[1]
    x_n = (x_val - x_min)/(x_max - x_min)
    y_val = (x_n * (y_max - y_min)) + y_min
    return y_val

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master, screen_width, screen_height):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = customtkinter.CTkFrame(master=self)
        self.main_frame.grid(row=0, column=0, padx=5, pady=5, sticky="news")

        self.label_title = customtkinter.CTkLabel(master=self.main_frame, text="WL", fg_color="transparent",
                                                  font=("Segoe UI", 20, 'bold'))
        self.label_title.grid(row=0, column=0, rowspan=3, padx=(5, 0), pady=(5, 5), sticky="news")

        self.label_brightness_color = customtkinter.CTkLabel(master=self.main_frame, text="Brightness & Color", fg_color="transparent",
                                                  font=("Segoe UI", 17, 'bold'))
        self.label_brightness_color.grid(row=0, column=1, rowspan=1, padx=(5, 0), pady=(5, 0), sticky="news")

        self.slider_intensity = customtkinter.CTkSlider(master=self.main_frame, orientation="horizontal", from_=0, to=100,
                                                        button_color="#808080",button_hover_color="#808080", progress_color="#808080")
        self.slider_intensity.grid(row=1, column=1, rowspan=1, padx=5, pady=(0, 5), sticky="we")

        self.slider_warm_cold = customtkinter.CTkSlider(master=self.main_frame, orientation="horizontal", from_=0, to=100,
                                                        button_color="#c9d9ff",button_hover_color="#c9d9ff", progress_color="#c9d9ff")
        self.slider_warm_cold.grid(row=2, column=1, rowspan=1, padx=5, pady=(5, 10), sticky="we")



        self.btn_on_off = customtkinter.CTkButton(master=self.main_frame, text="On/Off", font=("Segoe UI", 12, 'bold'),
                                                  width=55, height=25, corner_radius=5, border_width=1,
                                                  border_color="#c9d9ff", fg_color="#262626", hover_color="#808080")
        self.btn_on_off.grid(row=0, column=2, rowspan=1, padx=5, pady=(1, 2), sticky="we")

        self.btn_sendintensity = customtkinter.CTkButton(master=self.main_frame, text="Brightness", font=("Segoe UI", 12, 'bold'),
                                                         width=55, height=25, corner_radius=5, border_width=1,
                                                         border_color="#c9d9ff", fg_color="#262626", hover_color="#808080")
        self.btn_sendintensity.grid(row=1, column=2, rowspan=1, padx=5, pady=(1, 2), sticky="we")

        self.btn_sendgradient = customtkinter.CTkButton(master=self.main_frame, text="Gradient", font=("Segoe UI", 12, 'bold'),
                                                        width=55, height=25, corner_radius=5, border_width=1,
                                                        border_color="#c9d9ff", fg_color="#262626", hover_color="#808080")
        self.btn_sendgradient.grid(row=2, column=2, rowspan=1, padx=5, pady=(2, 1), sticky="we")

    def intensity_event(self, value):
        wb = int(map_valrange(value, (0, 100), (55, 200))) # From [0-100] to 55-200
        wb_color = f"#{wb:02x}{wb:02x}{wb:02x}"
        self.slider_intensity.configure(button_color=wb_color, button_hover_color=wb_color, progress_color=wb_color)

    def cold_hot_event(self, value):
        with open("data.json") as f:
            hot_map = json.load(f)["hot_cold_map"]

        hm_idx = int(map_valrange(value, (0, 100), (0, (len(hot_map) - 20))))
        color = hot_map[hm_idx]["hex"]
        self.slider_warm_cold.configure(button_color=color, button_hover_color=color, progress_color=color)

class App_GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Get screen resolution
        root = tkinter.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()

        # Optional but recommended: make window responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title("WiZLamp")
        self.main_frame = MainFrame(self, screen_width, screen_height)
        self.main_frame.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

if __name__ == "__main__":
    # Start main application
    main_app = App_GUI()
    main_app.mainloop()
    print(main_app.main_frame.slider_intensity.get())