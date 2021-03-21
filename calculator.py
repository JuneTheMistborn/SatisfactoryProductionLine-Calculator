# Satisfactory production line calculator
# Author: June Simmons
# 3/21/2021
# Allows calculation of how many items you need to input at a given overclock percentage,
# or the overclock percentage to create the given number of items,
# given how many items per minute it (needs/produces) at given overclock percentage

from tkinter import *
from PIL import ImageTk, Image

# Initializing window
root = Tk()
root.title("Satisfactory Production Calculator")
root.configure(bg="#5f668c")
root.attributes("-fullscreen", True)


# Defining function to be called on quit button press and function to validate the input number for overclock percentage
def Close():
    root.destroy()


def ValidateOverclock(overclock_var):
    if overclock_var.islower() or overclock_var.isupper():
        return False
    elif 250 >= overclock_var >= 0:
        return f"{(round(float(overclock_var), 4)):.4f}%"
    else:
        return False


# Placing the background image in the center of the screen
canvas = Canvas(root, width=850, height=778, bg="#fff", highlightthickness=0)
img = ImageTk.PhotoImage(Image.open("Recipe.png"))
canvas.create_image(0, 0, anchor=NW, image=img)
canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

# Entry based overclocking
overclockVar = 0.0
overclockIn = Entry(fg="#e59345", width=9)
overclockIn.place(x=710, y=734)

# Slider based overclocking
overclockSlider = Scale(bg="#fff", troughcolor="#fa9549", from_=0.0, to=250.0, bd=5, tickinterval=50.0,
                        orient="horizontal", sliderlength=10, length=500, width=45, highlightthickness=0)
overclockSlider.set(100)
overclockSlider.place(x=705, y=766)

exitBtn = Button(root, text="Quit", command=Close, bg="#e41b1e", activebackground="#e41b1e")
exitBtn.place(x=0, y=0)

root.mainloop()
