#https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowpos
#https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow

import tkinter as tk
from ctypes import windll
from builder import new_button

class CustomWindow:
    def __init__(self, title="Untitled Window", dimension=(300, 300)):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        
        self.title = title
        self.dimension = dimension
        self.maximized = False
        self.previous_position = [0, 0]
        self.hasstyle = False
        self.setup_window()

    def setup_window(self):
        """
        Creates the window and sets the initial geometry
        """
        self.set_initial_geometry()
        self.set_appwindow()
        self.create_title_bar()
        self.create_main_area()
        
        
        self.root.mainloop()

    
    def set_appwindow(self):
        '''
        Set the window style to app window style so that the window will appear in the taskbar
        and will not be hidden when the parent window is minimized
        '''
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        if not self.hasstyle:
            hwnd = windll.user32.GetParent(self.root.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style & ~WS_EX_TOOLWINDOW | WS_EX_APPWINDOW
            windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            self.root.withdraw()
            self.root.after(10, lambda: self.root.wm_deiconify())
            self.hasstyle = True


    def set_initial_geometry(self):
        x = (self.root.winfo_screenwidth() / 2) - (self.dimension[0] / 2)
        y = (self.root.winfo_screenheight() / 2) - (self.dimension[1] / 2)
        self.root.geometry(f'{self.dimension[0]}x{self.dimension[1]}+{int(x)}+{int(y)}')
        self.root.minsize(self.dimension[0], self.dimension[1])
        self.previous_position = [int(x), int(y)]

    def create_title_bar(self):
        back_ground = "#2c2c2c"
        self.title_bar = tk.Frame(self.root, bg=back_ground, bd=1, highlightthickness=0)
        self.title_name = tk.Label(self.title_bar, text=self.title, font=["Arial", 12], bg=back_ground, fg="white")
        
        self.minimize_btn = new_button(parent=self.title_bar, text='🗕', command=self.minimize)
        self.maximize_btn = new_button(parent=self.title_bar, text='🗖', command=self.maximize_toggle)
        self.close_btn = new_button(parent=self.title_bar, text='🗙', command=self.quit)

        self.title_bar.pack(fill='x', side=tk.TOP)
        self.title_name.pack(side='left', padx=5)
        self.close_btn.pack(side='right')
        
        self.maximize_btn.pack(side='right')
        self.minimize_btn.pack(side='right')

        self.title_bar.bind("<B1-Motion>", self.move_window)
        self.title_bar.bind("<Button-1>", self.get_pos)



    def create_main_area(self):
        self.window = tk.Frame(self.root, bg="white", highlightthickness=1, highlightbackground="#2c2c2c")
        txt = tk.Label(self.window, bg='white', text="Prototype window").pack(anchor="center")
        self.window.pack(fill='both', expand=True, side=tk.TOP)

    def get_pos(self, event):
        self.xwin = event.x
        self.ywin = event.y

    def move_window(self, event):
        self.root.geometry(f'+{event.x_root - self.xwin}+{event.y_root - self.ywin}')
        self.previous_position = [self.root.winfo_x(), self.root.winfo_y()]

    def minimize(self):
        hwnd = windll.user32.GetParent(self.root.winfo_id())
        windll.user32.ShowWindow(hwnd, 2)  # SW_MINIMIZE

    def maximize_toggle(self):
        hwnd = windll.user32.GetParent(self.root.winfo_id())
        if not self.maximized:
            self.maximize_btn.config(text="❐")
            windll.user32.SetWindowPos(hwnd, 0, 0, 0, 
                                        int(self.root.winfo_screenwidth()), 
                                        int(self.root.winfo_screenheight()-48), 0x40)
            self.maximized = True
        else:
            self.maximize_btn.config(text="🗖")
            windll.user32.SetWindowPos(hwnd, 0, self.previous_position[0],
                                        self.previous_position[1],
                                        int(self.root.minsize()[0]),
                                        int(self.root.minsize()[1]), 0x40)
            self.maximized = False

    def quit(self):
        self.root.destroy()

# Usage
if __name__ == "__main__":
    app = CustomWindow(title="My Custom Window", dimension=(400, 300))

