# check this code first.
from tkinter import *

app = Tk()
# The title of the project
app.title("Odiva: The Mask Detector")
# The size of the window
app.geometry("400x200")

# Defining a funtion
def c():
    # Label
    #m = Label(app, text="Text")
    #m.pack()


# Button
l = Button(app, text="Install Odiva", command=c)
# Packing the Button
l.pack()
app.mainloop()
