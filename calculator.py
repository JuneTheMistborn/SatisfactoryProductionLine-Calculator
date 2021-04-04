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
import re


# Custom entry with hint/placeholder
class Hintry(tk.Entry):
    def __init__(self, master=None, hint="Hint", color="grey", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.hint = hint

        self.fg_color = self["fg"]
        self.hint_color = color

        self.bind("<FocusIn>", self.clear_hint)
        self.bind("<FocusOut>", self.renew_hint)

        self.input_hint()

    def input_hint(self):
        self.insert("0", self.hint)
        self["fg"] = self.hint_color

    def clear_hint(self, a):
        if self["fg"] == self.hint_color:
            self.delete("0", "end")
            self["fg"] = self.fg_color

    def renew_hint(self, a):
        if not self.get():
            self.input_hint()


# Initializing window
class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.minsize(850, 778)
        self.root.title("Satisfactory Production Calculator")
        self.root.configure(bg="#5F668C")

        # Placing the background image in the center of the screen
        self.canvas = tk.Canvas(self.root, width=850, height=778, highlightthickness=0)
        self.img = ImageTk.PhotoImage(Image.open("Recipe.png"))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Entry based overclocking
        self.overclockIn = tk.Entry(master=self.canvas, bd=0, fg="#E59345", width=9,
                                    font=tk.font.Font(family="Myriad Pro", size=20))
        self.overclockIn.insert(0, "100.0000%")
        self.overclockIn.place(x=175, y=593)

        self.root.bind("<Return>", (lambda event: self.ValidateOverclock(self.overclockIn.get())))

        self.overclockValid = tk.Label(master=self.canvas, bd=0, fg="#278E3A",
                                       text="The overclock percentage is valid!")
        self.overclockValid.place(x=435, y=593)

        # Slider based overclocking
        self.overclockSlider = tk.Scale(master=self.canvas, command=self.ValidateOverclock, troughcolor="#FA9549",
                                        orient="horizontal", from_=0.0, to=250.0, length=500, width=45, sliderlength=10,
                                        bd=5, highlightthickness=0, tickinterval=50.0, showvalue=0)
        self.overclockSlider.set(100)
        self.overclockSlider.place(x=170, y=639)

        # Frames to hold input/output entries and labels so they properly resize
        self.inputAFrame = tk.Frame(master=self.canvas, bd=0)
        self.inputBFrame = tk.Frame(master=self.canvas, bd=0)
        self.inputCFrame = tk.Frame(master=self.canvas, bd=0)
        self.inputDFrame = tk.Frame(master=self.canvas, bd=0)
        self.outputAFrame = tk.Frame(master=self.canvas, bd=0)
        self.outputBFrame = tk.Frame(master=self.canvas, bd=0)

        # All entries for in and output amounts
        self.entryFont = tk.font.Font(family="Myriad Pro", size=8)
        self.validateIsNum = self.root.register(self.ValidateIsNum)

        self.inputA = Hintry(master=self.inputAFrame, hint="?", bd=0, fg="#E7994F", width=1, font=self.entryFont,
                             validate="key", validatecommand=(self.validateIsNum, "%S"))
        self.inputA.bind("<Key>", self.EntryResize)

        self.inputB = tk.Entry(bd=0, fg="#E7994F", width=9, font=self.entryFont)
        self.inputB.bind("<Key>", self.EntryResize)

        self.inputC = tk.Entry(bd=0, fg="#E7994F", width=9, font=self.entryFont)
        self.inputC.bind("<Key>", self.EntryResize)

        self.inputD = tk.Entry(bd=0, fg="#E7994F", width=9, font=self.entryFont)
        self.inputD.bind("<Key>", self.EntryResize)

        self.outputA = Hintry(master=self.canvas, hint="?", bd=0, fg="#E7994F", width=9, font=self.entryFont)
        self.outputA.bind("<Key>", self.EntryResize)

        self.outputB = tk.Entry(bd=0, fg="#E7994F", width=9, font=self.entryFont)
        self.outputB.bind("<Key>", self.EntryResize)

        # Placing input and output frames, packing input and output entries and labels into them
        self.inputAFrame.place(x=97, y=200)
        self.inputA.pack()
        #self.inputB.place()
        #self.inputC.place()
        #self.inputD.place()
        self.outputA.place(x=575, y=300)
        #self.outputB.place()

        self.root.mainloop()

    # Function to validate the input number for overclock percentage
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
                self.root.bell()
                self.overclockValid.configure(text="The overclock percentage is not valid!\nPlease enter a float "
                                                   "between 0 and 250\nwith 4 or less decimal places.", fg="#B42E2C")
        except ValueError:
            self.root.bell()
            self.overclockValid.configure(text="The overclock percentage is not valid!\nPlease enter a float between 0 "
                                               "and 250\nwith 4 or less decimal places.", fg="#B42E2C")

    # Function to validate the inserted text is a number
    def ValidateIsNum(self, inText):
        if re.search("[?.\d]", inText):
            return True
        else:
            self.root.bell()
            return False

    @staticmethod
    # Function to resize entry based on inserted text
    def EntryResize(event):
        if re.search("period", event.keysym) or re.search("\d", event.keysym):
            event.widget.configure(width=len(event.widget.get())+1)
        elif re.search("BackSpace", event.keysym):
            event.widget.configure(width=len(event.widget.get())-1)


if __name__ == "__main__":
    app = Calculator()
