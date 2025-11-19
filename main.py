import tkinter as tk

from core.app import App
from core.settings.logger import init_logger_minimal
import argparse

def main():

    parser = argparse.ArgumentParser(description='Enhanced Image Converter')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    args = parser.parse_args()

    init_logger_minimal(verbose=args.verbose, color=not args.no_color)

    root: tk.Tk = tk.Tk()
    app = App(root)

    app.root.mainloop()

if __name__ == "__main__":
    main()