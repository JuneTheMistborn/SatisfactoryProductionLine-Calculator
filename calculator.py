"""
Satisfactory production line calculator
Author: June Simmons
03/21/2021 - 05/27/2021
Allows calculation of how many items you need to input at a given overclock percentage,
or the overclock percentage to create the given number of items,
given how many items per minute it (needs/produces) at given overclock percentage
"""

import tkinter as tk
from PIL import ImageTk, Image
import tkinter.font as tkFont
import re


class Resizentry(tk.Entry):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.bind("<Key>", lambda a: self.resize(a.keysym, a.char))

    def resize(self, key, char):
        if key == "Left" or key == "Right":
            pass
        elif char != "\x08":
            self["width"] = len(self.get()) + 1
        elif char == "\x08":
            self["width"] = len(self.get()) - 1


# Custom entry with hint/placeholder
class Hintry(Resizentry):
    def __init__(self, master=None, hint="Hint", color="grey", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.hint = hint

        self.fg_color = self["fg"]
        self.hint_color = color

        self.bind("<FocusIn>", lambda a: self.clear_hint())
        self.bind("<FocusOut>", lambda a: self.renew_hint())

        self.input_hint()

    def input_hint(self):
        self.insert("0", self.hint)
        self["fg"] = self.hint_color
        self["width"] = len(self.hint)

    def clear_hint(self):
        if self["fg"] == self.hint_color:
            self.delete("0", "end")
            self["fg"] = self.fg_color

    def renew_hint(self):
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
        self.validateCommand = self.root.register(self.ValidateOverclock)
        self.overclockIn = Resizentry(master=self.canvas, bd=0, fg="#E59345", width=9, validate="key",
                                      bg="SystemButtonFace", validatecommand=(self.validateCommand, "%P"),
                                      font=tk.font.Font(family="Myriad Pro", size=20))
        self.overclockIn.place(x=175, y=593)

        # Slider based overclocking
        self.overclockSlider = tk.Scale(master=self.canvas, command=self.SliderToEntry, troughcolor="#FA9549",
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

        # All entries for input/output amounts
        self.entryFont = tk.font.Font(family="Myriad Pro", size=8)
        self.validateIsNum = self.root.register(self.ValidateIsNum)

        self.inputA100 = Hintry(master=self.canvas, hint="Items per min at 100%", bd=0, fg="#E7994F", width=1,
                                font=self.entryFont, name="inputA100", bg="SystemButtonFace",
                                validate="key", validatecommand=(self.validateIsNum, "%P", "%W", "%S"))

        self.inputB100 = Hintry(master=self.canvas, hint="Items per min at 100%", bd=0, fg="#E7994F", width=1,
                                font=self.entryFont, name="inputB100", bg="SystemButtonFace",
                                validate="key", validatecommand=(self.validateIsNum, "%P", "%W", "%S"))

        self.inputC100 = Hintry(master=self.canvas, hint="Items per min at 100%", bd=0, fg="#E7994F", width=1,
                                font=self.entryFont, name="inputC100", bg="SystemButtonFace",
                                validate="key", validatecommand=(self.validateIsNum, "%P", "%W", "%S"))

        self.inputD100 = Hintry(master=self.canvas, hint="Items per min at 100%", bd=0, fg="#E7994F", width=1,
                                font=self.entryFont, name="inputD100", bg="SystemButtonFace",
                                validate="key", validatecommand=(self.validateIsNum, "%P", "%W", "%S"))

        self.outputA = Hintry(master=self.outputAFrame, hint="?", bd=0, fg="#E7994F", width=1, font=self.entryFont,
                              validate="key", validatecommand=(self.validateIsNum, "%P", "%W", "%S"), name="outputA",
                              bg="SystemButtonFace")

        self.outputA100 = Hintry(master=self.canvas, hint="Items per min at 100%", bd=0, fg="#E7994F", width=1,
                                 font=self.entryFont, name="outputA100", bg="SystemButtonFace",
                                 validate="key", validatecommand=(self.validateIsNum, "%P", "%W", "%S"))

        self.outputB = Hintry(master=self.outputBFrame, hint="?", bd=0, fg="#E7994F", width=1, font=self.entryFont,
                              validate="key", validatecommand=(self.validateIsNum, "%P", "%W", "%S"), name="outputB",
                              bg="SystemButtonFace")

        self.outputB100 = Hintry(master=self.canvas, hint="Items per min at 100%", bd=0, fg="#E7994F", width=1,
                                 font=self.entryFont, name="outputB100", bg="SystemButtonFace",
                                 validate="key", validatecommand=(self.validateIsNum, "%P", "%W", "%S"))

        # Input text containers
        self.inputA = tk.Label(master=self.inputAFrame, bd=0, fg="#787879", text="?")
        self.inputB = tk.Label(master=self.inputBFrame, bd=0, fg="#787879", text="?")
        self.inputC = tk.Label(master=self.inputCFrame, bd=0, fg="#787879", text="?")
        self.inputD = tk.Label(master=self.inputDFrame, bd=0, fg="#787879", text="?")

        # All "per minute" labels for input/output
        self.perMinA = tk.Label(master=self.inputAFrame, bd=0, fg="#787879", text=" per minute")
        self.perMinB = tk.Label(master=self.inputBFrame, bd=0, fg="#787879", text=" per minute")
        self.perMinC = tk.Label(master=self.inputCFrame, bd=0, fg="#787879", text=" per minute")
        self.perMinD = tk.Label(master=self.inputDFrame, bd=0, fg="#787879", text=" per minute")
        self.perMinE = tk.Label(master=self.outputAFrame, bd=0, fg="#787879", text=" per minute")
        self.perMinF = tk.Label(master=self.outputBFrame, bd=0, fg="#787879", text=" per minute")

        # Placing input and output frames, packing input/output entries and labels into them
        self.inputA100.place(x=153, y=182)
        self.inputAFrame.place(x=99, y=200)
        self.inputA.pack(side="left")
        self.perMinA.pack(side="right")

        self.inputB100.place(x=153, y=266)
        self.inputBFrame.place(x=99, y=284)
        self.inputB.pack(side="left")
        self.perMinB.pack(side="right")

        self.inputC100.place(x=153, y=358)
        self.inputCFrame.place(x=99, y=376)
        self.inputC.pack(side="left")
        self.perMinC.pack(side="right")

        self.inputD100.place(x=153, y=434)
        self.inputDFrame.place(x=99, y=452)
        self.inputD.pack(side="left")
        self.perMinD.pack(side="right")

        self.outputA100.place(x=672, y=270)
        self.outputAFrame.place(x=604, y=288)
        self.outputA.pack(side="left")
        self.perMinE.pack(side="right")

        self.outputB100.place(x=672, y=354)
        self.outputBFrame.place(x=604, y=372)
        self.outputB.pack(side="left")
        self.perMinF.pack(side="right")

        # Variables to hold current value of entry, even if it has not been validated
        self.outputA100val = ""
        self.outputB100val = ""
        self.newOverclock = ""
        self.multiplier = 1
        self.editedWidget = ""

        # Modifying overclock entry at end as to have all necessary resources
        self.overclockIn.insert(0, "100.0000%")

        self.root.mainloop()

    # Method to set the overclock entry to the value of the slider
    def SliderToEntry(self, overclock_var):
        if self.overclockIn.get() != ".%":
            overclock_entry = float(self.overclockIn.get().strip("%"))
        else:
            overclock_entry = 0.0
        if overclock_var != str(round(overclock_entry)) and not overclock_entry > 250:
            self.overclockIn.delete("0", self.overclockIn.get().find("."))
            self.overclockIn.delete("1", self.overclockIn.get().find("%"))
            if overclock_entry > int(overclock_var) and overclock_entry != int(overclock_entry):
                self.overclockIn.insert(0, int(overclock_entry))
            elif overclock_entry > int(overclock_var) and overclock_entry == int(overclock_entry):
                self.overclockIn.insert(0, int(overclock_entry) - 1)
            elif overclock_entry < int(overclock_var):
                self.overclockIn.insert(0, int(overclock_entry) + 1)
            self.overclockIn.insert(self.overclockIn.get().find(".") + 1, "0000")

    # Method to validate the input number for overclock percentage
    def ValidateOverclock(self, new_overclock):
        if len(new_overclock) < 33 and re.fullmatch("\d*\.\d{0,4}%", new_overclock) and not new_overclock == ".%":
            self.NewMulti(new_overclock, "overclock", "")
            if float(new_overclock.strip("%")) >= 250:
                self.overclockSlider.set(250)
            else:
                self.overclockSlider.set(round(float(new_overclock.strip("%"))))
            return True
        elif new_overclock == ".%":
            self.overclockSlider.set(0)
            return True
        else:
            self.root.bell()
            return False

    # Method to validate the inserted text is a number
    def ValidateIsNum(self, in_text, widget, edit):
        if re.fullmatch("\d*\.?\d*|\?|Items per min at 100%|", in_text):
            if re.fullmatch("\d*\.?\d*", in_text):
                self.NewMulti(in_text, widget, edit)
            return True
        else:
            self.root.bell()
            return False

    # Method to calculate the input and overclock percentage
    def NewMulti(self, in_text, widget, edit):
        multiplier = 1
        # Finding what to multiply numbers by to get correct in/outputs
        try:
            if widget == "overclock" and re.fullmatch("\d*\.\d{0,4}%", in_text):
                multiplier = float(in_text.strip("%")) / 100
            elif re.search("outputA$", widget) and re.fullmatch("\d*\.?\d*", in_text):
                multiplier = float(in_text) / float(self.outputA100val)
            elif re.search("outputB$", widget) and re.fullmatch("\d*\.\d*", in_text):
                multiplier = float(in_text) / float(self.outputB100val)

            # Multiplying multiplier by numbers in 100% entries to get current in/output
            if float(in_text.strip("%")) / 100 == multiplier:
                pass
            elif float(self.overclockIn.get().strip("%")) / 100 != multiplier:
                self.newOverclock = str(float(self.overclockIn.get().strip("%")) * multiplier)
                self.overclockIn.delete(0, self.overclockIn.get().find("."))
                self.overclockIn.delete(1, self.overclockIn.get().find("%"))
                self.overclockIn.insert(0, self.newOverclock[0:self.newOverclock.find(".")])
                self.overclockIn.insert(self.newOverclock.find(".") + 1,
                                        (f"{float(self.newOverclock[self.newOverclock.find('.'):self.newOverclock.find('%')]):.4f}"[2:]))
        except ValueError:
            pass

        if re.fullmatch("\d*\.?\d*", in_text) and not re.fullmatch("", in_text) and re.search("outputA100", widget):
            self.editedWidget = widget
            self.outputA100val = in_text
            self.outputA.clear_hint()
            self.outputA.config(validate="none")
            self.outputA.delete(0, "end")
            self.outputA.insert(0, str(float(self.outputA100val) * multiplier))
            self.outputA.after_idle(self.ValidateSet, self.outputA)
            self.outputA.resize("", edit)

        if re.fullmatch("\d*\.?\d*", in_text) and not re.fullmatch("", in_text) and re.search("outputB100", widget):
            self.editedWidget = widget
            self.outputB100val = in_text
            self.outputB.clear_hint()
            self.outputB.config(validate="none")
            self.outputB.delete(0, "end")
            self.outputB.insert(0, str(float(in_text) * multiplier))
            self.outputB.after_idle(self.ValidateSet, self.outputB)
            self.outputB.resize("", edit)

        if re.fullmatch("\d*\.?\d*", in_text) and re.search("inputA100", widget):
            self.editedWidget = widget
            if in_text != "":
                self.inputA["fg"] = "#E7994F"
                self.inputA["text"] = str(float(in_text))
            elif in_text == "":
                self.inputA["fg"] = "grey"
                self.inputA["text"] = "?"

        '''if self.multiplier != multiplier:
            self.Calculate(multiplier, self.editedWidget)
        self.multiplier = multiplier'''

    # Calculate the new values of in/outputs based on multiplier and put them into the text/entries
    def Calculate(self, multiplier, widget):
        pass

    @staticmethod
    def ValidateSet(widget):
        widget.config(validate="key")


if __name__ == "__main__":
    app = Calculator()
