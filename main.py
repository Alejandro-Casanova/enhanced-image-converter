import tkinter as tk

from core.app import App
from core.settings.logger import init_logger_minimal

def main():
    init_logger_minimal(verbose=False, color=True)
    
    root: tk.Tk = tk.Tk()
    app = App(root)

    app.root.mainloop()

if __name__ == "__main__":
    main()