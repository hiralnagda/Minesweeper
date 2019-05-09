import tkinter as tk


class GUI(tk.Tk):
    def __init__(self, rows, cols, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.rect = {}
        self.oval = {}
        self.label = {}
        self.len = 25
        self.isopen = True
        self.canvas = tk.Canvas(self, width=self.len * cols, height=self.len * rows)
        col = 0
        self.canvas.pack(side="top", fill="both", expand="true")
        while col < cols:
            row = 0
            while row < rows:
                self.rect[row, col] = self.canvas.create_rectangle(
                    col * self.len, row * self.len, col * self.len + self.len, row * self.len + self.len, fill="white", tags="rect")
                self.label[row, col] = self.canvas.create_text(
                    col * self.len + 13, row * self.len + 13, fill='#000', text="", tags="label")
                row += 1
            col += 1

    def popup(self, loc):
        self.win = popup_window(self, loc)
        self.wait_window(self.win.top)

    def redraw(self, loc, val):
        if val != -2:
            self.canvas.itemconfig(self.rect[loc[0], loc[1]], fill="bisque3")
        else:
            val = "*"
            self.canvas.itemconfig(self.rect[loc[0], loc[1]], fill="red")
        self.canvas.itemconfig(self.label[loc[0], loc[1]], text=str(val))

    def endpopup(self, s):
        self.wait_window(end_window(self, s).top)

    def entry_value(self):
        if not hasattr(self.win, 'value'):
            self.destroy()
            return 10
        else:
            return self.win.value

    def on_close(self):
        self.isopen = False
        self.destroy()


class end_window(object):
    def __init__(self, master, s):
        self.master = master
        top = self.top = tk.Toplevel(master)
        self.l = tk.Label(top, text=s)
        self.l.pack()
        tk.Button(top, text='Ok', command=self.cleanup).pack()

    def cleanup(self):
        self.top.destroy()
        self.master.destroy()


class popup_window(object):
    def __init__(self, master, loc):
        top = self.top = tk.Toplevel(master)
        self.l = tk.Label(top, text="Enter value at location:" + str(loc))
        self.l.pack()
        self.e = tk.Entry(top)
        self.e.pack()
        tk.Button(top, text='Ok', command=self.cleanup).pack()

    def cleanup(self):
        self.value = self.e.get()
        self.top.destroy()

