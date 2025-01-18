import tkinter


class EntryComponent(tkinter.Entry):
    def __init__(self, parent, **kwargs):
        self.width = kwargs.get("width", 20)
        self.font = kwargs.get("font", ("arial", 10, "normal"))
        self.bg = kwargs.get("bg", "white")
        self.fg = kwargs.get("fg", "black")
        self.foreground_default = "gray"
        super().__init__(parent, width=self.width, font=self.font, bg=self.bg, fg=self.foreground_default)
        self.row = kwargs.get("row", 0)
        self.column = kwargs.get("column", 0)
        self.placeholder = kwargs.get("placeholder", "Enter the text")
        self.columnspan = kwargs.get("columnspan", 1)
        self.insert(0, self.placeholder)

        # Bind events
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        self.grid(row=self.row, column=self.column, columnspan=self.columnspan)

    def on_focus_in(self, event):
        """Remove placeholder when clicking inside the entry."""
        if self.get() == self.placeholder:
            self.delete(0, tkinter.END)
            self.config(foreground=self.fg)

    def on_focus_out(self, event):
        """Restore placeholder if entry is empty."""
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(foreground=self.foreground_default)

    def reset_entry(self, new_placeholder):
        self.delete(0, "end")
        self.insert(0, string=new_placeholder)
        self.config(fg="gray")
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def set_entry(self, new_placeholder):
        self.delete(0, "end")
        self.insert(0, string=new_placeholder)
        self.config(fg="black")

    def get_value(self):
        """Return actual user input, ignoring the placeholder."""
        if self.get() == self.placeholder:
            return ""  # Return empty string if placeholder is still visible
        return self.get()


class LabelComponent(tkinter.Label):
    def __init__(self, parent, **kwargs):
        self.text = kwargs.get("text", "Label")
        self.font = kwargs.get("font", ("arial", 10, "normal"))
        self.bg = kwargs.get("bg", "white")
        self.fg = kwargs.get("fg", "black")
        self.width = kwargs.get("width", 0)
        self.height = kwargs.get("height", 0)
        super().__init__(parent, text=self.text, width=self.width, height=self.height, font=self.font, bg=self.bg,
                         fg=self.fg)
        self.row = kwargs.get("row", 0)
        self.column = kwargs.get("column", 0)
        self.columnspan = kwargs.get("columnspan", 1)
        self.grid(row=self.row, column=self.column, columnspan=self.columnspan)

    def set_label(self, value):
        self["text"] = value


class TextComponent(tkinter.Text):
    def __init__(self, parent, **kwargs):
        self.font = kwargs.get("font", ("arial", 10, "normal"))
        self.bg = kwargs.get("bg", "white")
        self.fg = kwargs.get("fg", "black")
        self.width = kwargs.get("width", 0)
        self.height = kwargs.get("height", 0)
        self.padx = kwargs.get("padx", 0)
        self.pady = kwargs.get("pady", 0)
        super().__init__(parent, width=self.width, height=self.height, font=self.font, bg=self.bg, fg=self.fg)
        self.row = kwargs.get("row", 0)
        self.column = kwargs.get("column", 0)
        self.columnspan = kwargs.get("columnspan", 1)
        self.grid(row=self.row, column=self.column, columnspan=self.columnspan, padx=self.padx, pady=self.pady)


class ButtonComponent(tkinter.Button):
    def __init__(self, parent, **kwargs):
        # self.text = kwargs.get("text", "Label")
        self.text_var = tkinter.StringVar()
        self.text_var.set(kwargs.get("text", "Label"))
        self.font = kwargs.get("font", ("arial", 10, "normal"))
        self.bg = kwargs.get("bg", "white")
        self.fg = kwargs.get("fg", "black")
        self.width = kwargs.get("width", 20)
        self.command = kwargs.get("command")
        super().__init__(parent, textvariable=self.text_var, width=self.width, font=self.font, bg=self.bg, fg=self.fg,
                         command=self.command)
        self.row = kwargs.get("row", 0)
        self.column = kwargs.get("column", 0)
        self.columnspan = kwargs.get("columnspan", 1)
        self.grid(row=self.row, column=self.column, columnspan=self.columnspan)

    def edit_text_button(self, new_button_text):
        self.text_var.set(new_button_text)


class CanvasComponent(tkinter.Canvas):
    def __init__(self, parent, **kwargs):
        self.frame2 = None
        self.width = kwargs.get("width", 100)
        self.height = kwargs.get("height")
        self.photo = ""
        self.parent = parent
        super().__init__(parent, width=self.width, height=self.height)
        self.row = kwargs.get("row", 0)
        self.column = kwargs.get("column", 0)
        self.columnspan = kwargs.get("columnspan", 1)
        self.sticky = "nesw"
        self.grid(row=self.row, column=self.column, columnspan=self.columnspan, sticky=self.sticky)

    def create_canvas_image(self, x_coor, y_coor, image):
        self.photo = tkinter.PhotoImage(file=image)
        self.create_image(x_coor, y_coor, image=self.photo)

    def update_scroll_region(self, event=None):
        """Updates the scroll region of the canvas"""
        self.configure(scrollregion=self.bbox("all"))

    def create_scrollbar_grid(self, frame_name):
        self.frame2 = frame_name
        """Creates a scrollbar and a scrollable frame inside the canvas"""
        # Create vertical scrollbar
        scrollbar = tkinter.Scrollbar(self.parent, orient="vertical", command=self.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure canvas to use the scrollbar
        self.configure(yscrollcommand=scrollbar.set)

        self.create_window((0, 0), window=self.frame2, anchor="nw")

        # Bind frame resizing to update scroll region
        self.frame2.bind("<Configure>", lambda event: self.update_scroll_region())

        # Expand `canvas` within `parent`
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
