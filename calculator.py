# Satisfactory production line calculator
# Author: June Simmons
# 3/21/2021
# Allows calculation of how many items you need to input at a given overclock percentage,
# or the overclock percentage to create the given number of items,
# given how many items per minute it (needs/produces) at given overclock percentage

from tkinter import *
from PIL import ImageTk, Image


# Initializing window
class Calculator:
    def __init__(self):
        self.root = Tk()
        self.root.title("Satisfactory Production Calculator")
        self.root.configure(bg="#5F668C")
        self.root.attributes("-fullscreen", True)

        # Placing the background image in the center of the screen
        self.canvas = Canvas(self.root, width=850, height=778, highlightthickness=0)
        self.img = ImageTk.PhotoImage(Image.open("Recipe.png"))
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Entry based overclocking
        self.overclockIn = Entry(fg="#E59345", width=9)
        self.overclockIn.insert(0, "100.0000%")
        self.overclockIn.place(x=710, y=734)

        self.root.bind("<Return>", (lambda event: self.ValidateOverclock(self.overclockIn.get())))

        self.overclockValid = Label(bd=0, fg="#278E3A", text="The overclock percentage is valid!")
        self.overclockValid.place(x=770, y=734)

        # Slider based overclocking
        self.overclockSlider = Scale(command=self.ValidateOverclock, troughcolor="#FA9549", orient="horizontal",
                                     from_=0.0, to=250.0, length=500, width=45, sliderlength=10, bd=5,
                                     highlightthickness=0, tickinterval=50.0)
        self.overclockSlider.set(100)
        self.overclockSlider.place(x=705, y=766)

        self.exitBtn = Button(self.root, text="Quit", command=self.Close, bg="#E41B1E", activebackground="#e41b1e")
        self.exitBtn.place(x=0, y=0)

        self.root.mainloop()

    # Defining function to be called on quit button press and
    # function to validate the input number for overclock percentage
    def Close(self):
        self.root.destroy()

    def ValidateOverclock(self, overclock_var):
        try:
            if 250.0 >= float(overclock_var.strip("%")) >= 0.0:
                overclock = f"{(float(overclock_var.strip('%'))):.4f}"
                self.overclockValid.configure(text="The overclock percentage is valid!", fg="#278E3A")
                if float(overclock) == round(float(self.overclockIn.get().strip("%"))):
                    pass
                elif float(overclock) != round(float(self.overclockIn.get().strip("%"))):
                    self.overclockIn.delete(0, "end")
                    self.overclockIn.insert(0, overclock + "%")
                    self.overclockSlider.set(float(overclock))
            else:
                self.overclockValid.configure(text="The overclock percentage is not valid!\nPlease enter a float "
                                                   "between 0 and 250 with 4 or less decimal places.", fg="#B42E2C")
        except ValueError:
            self.overclockValid.configure(text="The overclock percentage is not valid!\nPlease enter a float between 0 "
                                               "and 250 with 4 or less decimal places.", fg="#B42E2C")


app = Calculator()
