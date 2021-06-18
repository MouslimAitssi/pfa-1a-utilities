from tkinter import *

root = Tk()
root.title("New app")
root.geometry("400x400")

heading = Label(root, text="My app", font = ("courrier", 35), fg = 'blue').pack()

label1 = Label(root, text="enter ur name:", font=("arial", 20, "bold"), fg="black").pack()
name = StringVar()
entry_box = Entry(root, textvariable=name, width=25, bg="lightgreen").pack()
def do_it():
	print("hello "+str(name.get()))
work = Button(root, text = "work", width=30, height=5, bg="lightblue", command=do_it).pack()
root.mainloop()	