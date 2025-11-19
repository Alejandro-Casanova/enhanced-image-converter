import tkinter as tk

from core.app import App

def main():
    root: tk.Tk = tk.Tk()
    app = App(root)

    app.root.mainloop()

if __name__ == "__main__":
    main()