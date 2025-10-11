import customtkinter
import tkinter
import json

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master, screen_width, screen_height):
        super().__init__(master)
        
        def intensity_event(value):
            """
            Formula for modifying range:
            x in [a,b]. We want x to be in [c,d]

            Normalized x: x_n = (x - a)/(b - a) in [0,1]
            y = x_n * (d-c) + c
            """
            wb = int((value / 100) * 200 + 55)  # From [0-100] to 55-200
            wb_color = f"#{wb:02x}{wb:02x}{wb:02x}"
            print(wb_color)
            self.slider_intensity.configure(button_color=wb_color, button_hover_color=wb_color, progress_color=wb_color)

        def cold_hot_event(value):
            with open("data.json") as f:
                hot_map = json.load(f)["hot_cold_map"]

            hm_idx = int((value/100) * (len(hot_map) - 1))
            color = hot_map[hm_idx]["hex"]
            self.slider_warm_cold.configure(button_color=color, button_hover_color=color, progress_color=color)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = customtkinter.CTkFrame(master=self)
        self.main_frame.grid(row=0, column=0, padx=5, pady=5, sticky="news")

        self.label_title = customtkinter.CTkLabel(master=self.main_frame, text="WL", fg_color="transparent",
                                                  font=("Helvetica", 20, 'bold'))
        self.label_title.grid(row=0, column=0, rowspan=2, padx=(5, 0), pady=(5, 5), sticky="news")

        self.slider_intensity = customtkinter.CTkSlider(master=self.main_frame, orientation="horizontal", from_=0, to=100,
                                                        button_color="#808080",button_hover_color="#808080", progress_color="#808080",
                                                        command=intensity_event)
        self.slider_intensity.grid(row=0, column=1, rowspan=1, padx=5, pady=(10, 5), sticky="we")

        self.slider_warm_cold = customtkinter.CTkSlider(master=self.main_frame, orientation="horizontal", from_=0, to=100,
                                                        button_color="#c9d9ff",button_hover_color="#c9d9ff", progress_color="#c9d9ff",
                                                        command=cold_hot_event)
        self.slider_warm_cold.grid(row=1, column=1, rowspan=1, padx=5, pady=(5, 10), sticky="we")

class App(customtkinter.CTk):
    def __init__(self, screen_width: int, screen_height: int):
        super().__init__()

        # Optional but recommended: make window responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title("WiZLamp")
        self.main_frame = MainFrame(self, screen_width, screen_height)
        self.main_frame.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

if __name__ == "__main__":
    # Get screen resolution
    root = tkinter.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()

    # Start main application
    main_app = App(screen_width=width, screen_height=height)
    main_app.mainloop()
    print(main_app.main_frame.slider_intensity.get())