import tkinter as tk
import csv
import os
import tkinter.ttk as ttk

#main class which holds parent frame where other pages are stored
class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.title(self, string = "OVG Sales Calculator")

        main_container = tk.Frame(self)
        main_container.pack()
        
        self.frames = {}
        
        for page in (FileOpenPage, CalculationsPage):
            frame = page(main_container, self)
            self.frames[page] = frame
            frame.grid(row = 0, sticky = tk.NSEW)
    
        self.show_frame(FileOpenPage)

    #this method will show the page that we pass through
    #any existing frame grids are removed so that window will auto resize
    def show_frame(self, frame):
        for f in self.frames.values():
            f.grid_remove()
        frame_to_raise = self.frames[frame]
        frame_to_raise.grid()


#inital page that is shown in beginning.
#prompts user for a file
class FileOpenPage(tk.Frame):

    def __init__(self, parent_frame, parent_class):
        tk.Frame.__init__(self, parent_frame)
        
        label = ttk.Label(self, text = "Please open a file or create a new one")
        label.grid(row = 0)

        file_list = tk.Listbox(self)
        for f in os.listdir():
            if ".csv" in f:
                file_list.insert(tk.END, f)

        file_list.grid(row = 1)

        combo_frame = tk.Frame(self)
        combo_frame.grid(row = 1, column = 1, padx = 20)
        entry = ttk.Entry(combo_frame)
        entry.pack(side = tk.TOP)
        create_new_file = ttk.Button(combo_frame, text = "Create", command = lambda: self.create_new_file(entry.get(), parent_class))
        create_new_file.pack(side = tk.BOTTOM)

        open_file = ttk.Button(self, text = "Open", command = lambda: self.open_file(file_list.get(tk.ANCHOR), parent_class))
        open_file.grid(row = 2, pady = 20)


    def open_file(self, selection, parent_class):
        CalculationsPage.set_file_name(selection)
        parent_class.show_frame(CalculationsPage)

    def create_new_file(self, new_file_name, parent_class):
        with open(f"{new_file_name}.csv", "x") as f:
            pass
        CalculationsPage.set_file_name(f"{new_file_name}.csv")
        parent_class.show_frame(CalculationsPage)


#page shown after file open page
#asks user for data to be inputted and saved to csv
class CalculationsPage(tk.Frame):
    categories = ["Date", "Non-Tax Sales", "Taxable Sales", "Lotto", "Lotto Payout",
                    "Card Fee", "Discounts", "Misc.", "Net"]
    file_name = ""

    def __init__(self, parent_frame, parent_class):
        widgets = []

        tk.Frame.__init__(self, parent_frame)

        for i in range(9):
            if i == 8:
                net_label = ttk.Label(self, text = CalculationsPage.categories[i])
                net_label.grid(row = 8, column = 1, padx = 40, pady = 1)

                net_message = ttk.Label(self)
                net_message.grid(row = 8, column = 2, padx = 20, pady = 1)

                widgets.append(net_message)
            else:
                label = ttk.Label(self, text = CalculationsPage.categories[i])
                label.grid(row = i, column = 1, padx = 40, pady = 1)

                entry = ttk.Entry(self)
                entry.grid(row = i, column = 2, padx = 20, pady = 1)

                widgets.append(entry)

        calc_button = ttk.Button(self, text = "Calculate", command = lambda: self.calculate(widgets))
        calc_button.grid(row = 9, padx = 40)

        submit_button = ttk.Button(self, text = "Submit", command = lambda: self.submit(widgets))
        submit_button.grid(row = 9, column = 1)

        clear_button = ttk.Button(self, text = "Clear", command = lambda: self.clear(widgets))
        clear_button.grid(row = 9, column = 2)

        back_button = ttk.Button(self, text = "Back", command = lambda: self.back(parent_class))
        back_button.grid(row = 0, padx = 20, pady = 5)
        
    def clear(self, widgets):
        for widget in widgets:
            if widgets.index(widget) == len(widgets) - 1:
                widget.config(text = "")
            else:
                widget.delete(0, tk.END)

    def calculate(self, widgets):
        sum = 0
        for widget in widgets[1:]:
            if widgets.index(widget) == len(widgets) - 1:
                widget.config(text = f"{sum}")
            else:
                if widget.get().strip() != "":
                    try:
                        sum += float(widget.get())
                    except:
                        error = tk.Toplevel(width = 100, height = 100)
                        message = tk.Message(error,
                                             text = f"{CalculationsPage.categories[widgets.index(widget)]} is not a number! Try again")
                        message.grid(row = 0, padx = 5, pady = 5)
                        dismiss = ttk.Button(error, text = "Dismiss", command = error.destroy)
                        dismiss.grid(row = 1, padx = 5, pady = 5)
                        error.mainloop()

    def submit(self, widgets):
        with open(f"{CalculationsPage.file_name}", "a", newline = '') as file:
            writer = csv.writer(file)
            row = []
            for widget in widgets:
                if widgets.index(widget) != len(widgets) - 1:
                    row.append(widget.get())
                else:
                    row.append(widget.cget("text"))
            writer.writerow(row) 

    def back(self, parent_class):
        parent_class.show_frame(FileOpenPage)

    @classmethod
    def set_file_name(cls, file_name):
        CalculationsPage.file_name = file_name


calculator = App()
calculator.mainloop()
