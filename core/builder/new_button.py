# builder/button_builder.py

import tkinter as tk

def new_button(parent: tk.Widget, 
                text: str, command, 
                bg: str = "#2c2c2c", 
                fg: str = "white", 
                width: int = 2, 
                font: str = "bold") -> tk.Button:
    """
    Creates a styled button.

    Parameters:
    - parent: The parent widget (usually a Frame or Window).
    - text: The text to display on the button.
    - command: The function to call when the button is pressed.
    - bg: The background color of the button.
    - fg: The foreground (text) color of the button.
    - width: The width of the button.
    - font: The font style of the button text.

    Returns:
    A Tkinter Button widget.
    """
    btn = tk.Button(parent, text=text, bg=bg, padx=5, pady=2,
                    bd=0, font=font, fg=fg, width=width,
                    activebackground="red", activeforeground="white",
                    highlightthickness=0, command=command)
    
    btn.bind('<Enter>', lambda x: btn.configure(bg='#777777'))
    btn.bind('<Leave>', lambda x: btn.configure(bg=bg))
    
    return btn
