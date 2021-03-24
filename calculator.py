"""
Satisfactory production line calculator
Author: June Simmons
3/21/2021
Allows calculation of how many items you need to input at a given overclock percentage,
or the overclock percentage to create the given number of items,
given how many items per minute it (needs/produces) at given overclock percentage
"""

import tkinter as tk
from PIL import ImageTk, Image
import tkinter.font as tkFont


# Initializing window
class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.minsize(850, 778)
        self.root.title("Satisfactory Production Calculator")
        self.root.configure(bg="#5F668C")
        self.root.bind('<Configure>', self.Resize)

        # Placing the background image in the center of the screen
        self.canvas = tk.Canvas(self.root, width=850, height=778, highlightthickness=0)
        self.img = ImageTk.PhotoImage(Image.open("Recipe.png"))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Entry based overclocking
        self.font = tk.font.Font(family="Myriad Pro", size=20)
        self.overclockIn = tk.Entry(bd=0, fg="#E59345", width=9, font=self.font)
        self.overclockIn.insert(0, "100.0000%")
        self.overclockIn.place(x=175, y=593)

        self.root.bind("<Return>", (lambda event: self.ValidateOverclock(self.overclockIn.get())))

        self.overclockValid = tk.Label(bd=0, fg="#278E3A", text="The overclock percentage is valid!")
        self.overclockValid.place(x=435, y=593)

        # Slider based overclocking
        self.overclockSlider = tk.Scale(command=self.ValidateOverclock, troughcolor="#FA9549", orient="horizontal",
                                        from_=0.0, to=250.0, length=500, width=45, sliderlength=10, bd=5,
                                        highlightthickness=0, tickinterval=50.0, showvalue=0)
        self.overclockSlider.set(100)
        self.overclockSlider.place(x=170, y=639)

        self.root.mainloop()

    # function to validate the input number for overclock percentage

    def Resize(self, wh):
        w = (1920-self.root.winfo_width())/2
        h = (1040-self.root.winfo_height())/2
        self.overclockIn.place(x=710-w, y=724-h)
        self.overclockValid.place(x=970-w, y=724-h)
        self.overclockSlider.place(x=705-w, y=770-h)

    def ValidateOverclock(self, overclock_var):
        try:
            if 250.0 >= float(overclock_var.strip("%")) >= 0.0:
                overclock = f"{(float(overclock_var.strip('%'))):.4f}"
                self.overclockValid.configure(text="The overclock percentage is valid!", fg="#278E3A")
                if float(overclock) == round(float(self.overclockIn.get().strip("%"))):
                    self.overclockSlider.set(float(overclock))
                elif float(overclock) != round(float(self.overclockIn.get().strip("%"))):
                    self.overclockIn.delete(0, "end")
                    self.overclockIn.insert(0, overclock + "%")

            else:
                self.overclockValid.configure(text="The overclock percentage is not valid!\nPlease enter a float "
                                                   "between 0 and 250\nwith 4 or less decimal places.", fg="#B42E2C")
        except ValueError:
            self.overclockValid.configure(text="The overclock percentage is not valid!\nPlease enter a float between 0 "
                                               "and 250\nwith 4 or less decimal places.", fg="#B42E2C")


app = Calculator()
