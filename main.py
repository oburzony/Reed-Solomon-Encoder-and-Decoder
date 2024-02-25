import tkinter as tk
import ui_manager 
import encoder

def main():
    data = [0, 0, 0, 0, 0, 0, 0, 0, 1]
    encoder.rs_encode(data) 

    root = tk.Tk()
    ui_manager.ui_config(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()