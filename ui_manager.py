import tkinter as tk
import encoder
import decoder

def validate_entry_encode(text):
    if not text:
        return True
    parts = text.split(', ')
    if len(parts) > 9: 
        return False
    if not all((part.isdigit() and 0 <= int(part) <= 15) or not part for part in parts):
        return False
    return True

def validate_entry_decode(text):
    if not text:
        return True
    parts = text.split(', ')
    if len(parts) > 15:  
        return False
    if not all((part.isdigit() and 0 <= int(part) <= 15) or not part for part in parts):
        return False
    return True

def add_comma(event, entry):
    entry.insert(tk.INSERT, ', ')

def copy_result(ent_data_encode, ent_data_enter_decode):
    encoded_data = ent_data_encode.get()
    ent_data_enter_decode.config(state="normal") 
    ent_data_enter_decode.delete(0, tk.END) 
    ent_data_enter_decode.insert(0, encoded_data)

def encode_data(ent_data_encoded, ent_data, txt_console): 
    data_to_encode = ent_data.get()

    if not data_to_encode:
        txt_console.insert(tk.END, ">>> ERROR: Data to encode cannot be empty.\n")
        return
    
    data_to_encode_list = data_to_encode.split(', ')    

    if len(data_to_encode_list) != 9:
        txt_console.insert(tk.END, ">>> ERROR: Data to encode must contain exactly 9 numbers separated by commas and space.\n")
        return
    
    if not all(data.strip() for data in data_to_encode_list):
        txt_console.insert(tk.END, ">>> ERROR: Each number in the data to encode must be non-empty.\n")
        return
    
    data_to_encode_list = [int(x) for x in data_to_encode_list]
    encoded_data = encoder.rs_encode(data_to_encode_list) 
    encoded_data_str = ', '.join(str(x) for x in encoded_data)
    
    txt_console.insert(tk.END, "\n>>> START ENCODING\n")
    txt_console.insert(tk.END, ">>> DATA TO ENCODE:" + str(data_to_encode_list) + "\n")
    txt_console.insert(tk.END, ">>> ERROR CORRECTION PART:" + str(encoded_data[9:15]) + "\n")
    txt_console.insert(tk.END, ">>> ENCODED DATA:" + str(encoded_data) + "\n")

    ent_data_encoded.config(state="normal")  
    ent_data_encoded.delete(0, tk.END)     
    ent_data_encoded.insert(0, encoded_data_str)        
    ent_data_encoded.config(state="readonly") 

def decode_data(ent_data_decoded, ent_data, txt_console):
    data_to_decode = ent_data.get()

    if not data_to_decode:
        txt_console.insert(tk.END, ">>> ERROR: Data to encode cannot be empty.\n")
        return
    
    data_to_decode_list = data_to_decode.split(', ')  

    if len(data_to_decode_list) != 15:
        txt_console.insert(tk.END, ">>> ERROR: Data to encode must contain exactly 15 numbers separated by commas and space.\n")
        return
    
    if not all(data.strip() for data in data_to_decode_list):
        txt_console.insert(tk.END, ">>> ERROR: Each number in the data to encode must be non-empty.\n")
        return
    
    data_to_decode_list = [int(x) for x in data_to_decode_list]
    decoded_data = decoder.rs_decode(data_to_decode_list) 
    decoded_data_str = ', '.join(str(x) for x in decoded_data)

    txt_console.insert(tk.END, "\n>>> START DECODING\n")
    txt_console.insert(tk.END, ">>> DATA TO DECODE:" + str(data_to_decode_list) + "\n")
    txt_console.insert(tk.END, ">>> DECODED DATA:" + str(decoded_data) + "\n")

    ent_data_decoded.config(state="normal")  
    ent_data_decoded.delete(0, tk.END)     
    ent_data_decoded.insert(0, decoded_data_str)        
    ent_data_decoded.config(state="readonly") 

def write_instruction(txt_console):
    try:
        with open("instruction.txt", "r") as plik:
            zawartosc = plik.read()
            txt_console.insert(tk.END, zawartosc)
    except FileNotFoundError:
            print("Plik nie został znaleziony.")

def clear_data(ent_data):
    ent_data.delete(0, tk.END)        

def ui_config(root):
    root.title("Reed-Solomon (15,9) encoder and simplified decoder")
    window_width = 1280
    window_height = 720
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    root.resizable(True, True)

    # Frames
    frm_service = tk.Frame(root, bg="lightgray", bd=2, relief=tk.RAISED)
    frm_service.pack(fill=tk.Y, side=tk.LEFT)
    
    frm_console = tk.Frame(root, bg="black")
    frm_console.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    
    # Texts 
    txt_console = tk.Text(frm_console, bg="black", fg="white")
    txt_console.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    # Grid Layout Configuration
    frm_service.columnconfigure(0, weight=1, uniform='a')
    frm_service.rowconfigure(list(range(14)), weight=1, uniform='a') 

    # Labels
    label_widgets = [tk.Label(frm_service) for _ in range(4)]
    lbl_data_to_encode, lbl_data_encoded, lbl_data_to_decode, lbl_data_decoded = label_widgets

    label_configs = [
        (lbl_data_to_encode, "Enter data to encode (9 numbers [0-15]):"),
        (lbl_data_encoded, "Encoded data:"),
        (lbl_data_to_decode, "Enter data to decode (15 numbers [0-15]):"),
        (lbl_data_decoded, "Decoded data:")
    ]

    for i, (label, text) in enumerate(label_configs):
        label.config(text=text, bg="lightgray")
        label.grid(row=6 + 2 * i, sticky="ew", padx=2, pady=(0, 0))

    # Entries
    entry_widegts = [tk.Entry(frm_service) for _ in range(4)]
    ent_data_to_encode, ent_data_encoded, ent_data_to_decode, ent_data_decoded = entry_widegts

    entry_configs = [
        (ent_data_to_encode, {"validate": "key", "validatecommand": (frm_service.register(validate_entry_encode), "%P")}),
        (ent_data_encoded, {"state": "readonly"}),
        (ent_data_to_decode, {"validate": "key", "validatecommand": (frm_service.register(validate_entry_decode), "%P")}),
        (ent_data_decoded, {"state": "readonly"})
    ]

    for entry, config in entry_configs:
        entry.config(**config)
        if entry in (ent_data_to_encode, ent_data_to_decode):
            entry.bind('<KeyPress-space>', lambda event, e=entry: add_comma(event, e))

    for i, entry in enumerate(entry_widegts):
        entry.grid(row=6 + 2 * i + 1, sticky="ew", padx=2, pady=(0, 30))
    
    # Buttons 
    button_widgets = [tk.Button(frm_service) for _ in range(6)]
    btn_instruction, btn_data_encode, btn_data_decode, btn_data_copy_to_decode, btn_clear_encode, btn_clear_decode = button_widgets

    button_configs = [
    (btn_instruction,"Instruction", lambda: write_instruction(txt_console)),
    (btn_data_encode,"Encode", lambda: encode_data(ent_data_encoded,ent_data_to_encode, txt_console)),
    (btn_data_decode,"Decode", lambda: decode_data(ent_data_decoded, ent_data_to_decode, txt_console)),
    (btn_data_copy_to_decode,"Copy to Decode", lambda: copy_result(ent_data_encoded, ent_data_to_decode)),
    (btn_clear_encode, "Clear data to encode", lambda: clear_data(ent_data_to_encode)),
    (btn_clear_decode, "Clear data to decode", lambda: clear_data(ent_data_to_decode))
    ]

    for i, (button,text, command) in enumerate(button_configs):
        button.config(text=text, command=command)
        button.grid(row=i, sticky="nesw", padx=2, pady=2)

    
      
