from tkinter import *

window = Tk()

listbox = Listbox(window, selectmode = 'multiple', font = ('Tahoma', 8)).pack()

text = 'لاتللتاالا يالبتلبالن بلبتلبت '
listbox = listbox.decode('unicode-escape')
word = re.findall(u'word = .', TEXT, re.UNICODE)[0]
listbox.insert(END,)



window.mainloop()