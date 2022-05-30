from tkinter import *

root = Tk()


global input_text
input_text = StringVar()
input_text.set('0')

i = 0

def change():
    global i
    i += 1
    input_text.set('{}'.format(i))

lab = Label(root, textvariable = input_text).pack()
btn = Button(root, text = 'button', command = change)
btn.pack()
root.mainloop()