from tkinter import *

# master = Tk()
# master.minsize(400, 400)
# master.geometry("320x100")
#
#
# def callback():
#     print('Click')
#
#
# photo = PhotoImage(file="./ChessArt/BK.png")
# b = Button(master, image=photo, command=callback, height=50, width=50)
# b.pack()
#
# mainloop()


root = Tk()


for r in range(3):
   for c in range(4):
      Label(root, text='R%s/C%s'%(r,c),
         borderwidth=1 ).grid(row=r,column=c)


root.mainloop()