import tkinter as tk
import ui_manager 
import encoder

def main():
    data = [0, 0, 0, 0, 0, 0, 0, 0, 1]
    encoded_data = encoder.rs_encode(data) 
    print("\ENCODED DATA:")
    print(encoded_data)

    root = tk.Tk()
    ui_manager.ui_config(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()