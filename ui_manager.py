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
    labels = [
        "Enter data to encode (9 numbers [0-15]):",
        "Encoded data:",
        "Enter data to decode (15 numbers [0-15]):",
        "Decoded data:"
    ]
    label_objects = []

    for i, text in enumerate(labels):
        label_name = f"label_{i}"
        label_name = tk.Label(frm_service, text=text, bg="lightgray")
        label_name.grid(row= 6 + 2 * i  , sticky="ew", padx=2, pady=(0, 0))
        label_objects.append(label_name)

    # Entries
    entries = [tk.Entry(frm_service, validate="key", validatecommand=(frm_service.register(validate_entry_encode), "%P")) for _ in range(3)]
    entries[0].bind('<KeyPress-space>', lambda event: add_comma(event, entries[0]))
    entries[1]["state"] = "readonly"
    entries[2].bind('<KeyPress-space>', lambda event: add_comma(event, entries[2]))
    entries[2]["state"] = "readonly"

    for i, entry in enumerate(entries):
        entry.grid(row=6 + 2 * i + 1, sticky="ew", padx=2, pady=(0, 30))

    # Buttons
    button_texts = ["Instruction", "Encode", "Decode", "Copy to Decode", "Clear data to encode", "Clear data to decode"]
    button_commands = [lambda: write_instruction(txt_console), lambda: encode_data(entries[1], entries[0], txt_console),
                       lambda: decode_data(entries[2], entries[3], txt_console), lambda: copy_result(entries[1], entries[2]),
                       lambda: clear_data(entries[0]), lambda: clear_data(entries[2])]

    for i, (text, command) in enumerate(zip(button_texts, button_commands)):
        button = tk.Button(frm_service, text=text, command=lambda cmd=command: cmd(txt_console))
        button.grid(row=i, sticky="nesw", padx=2, pady=2)

      

"""
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
    frm_console = tk.Frame(root, bg="black")

    # Texts 
    txt_console = tk.Text(frm_console, bg="black", fg="white")
    txt_console.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    # Pack Placement
    frm_service.pack(fill=tk.Y, side=tk.LEFT)
    frm_console.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    
    txt_console.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    # Labels 
    lbl_data_to_encode = tk.Label(frm_service, text="Enter data to encode (9 numbers [0-15]):", bg="lightgray")  
    lbl_data_encoded = tk.Label(frm_service, text="Encoded data:", bg="lightgray")  
    lbl_data_to_decode = tk.Label(frm_service, text="Enter data to decode (15 numbers [0-15]):", bg="lightgray")  
    lbl_data_decoded = tk.Label(frm_service, text="Decoded data:", bg="lightgray")  

    # Entries
    ent_data_to_encode = tk.Entry(frm_service, validate="key", validatecommand=(frm_service.register(validate_entry_encode), "%P")) 
    ent_data_to_decode = tk.Entry(frm_service, validate="key", validatecommand=(frm_service.register(validate_entry_decode), "%P"))  
    ent_data_to_encode.bind('<KeyPress-space>', lambda event: add_comma(event, ent_data_to_encode))
    ent_data_to_decode.bind('<KeyPress-space>', lambda event: add_comma(event, ent_data_to_decode))
    ent_data_encoded = tk.Entry(frm_service, state="readonly") 
    ent_data_decoded = tk.Entry(frm_service, state="readonly") 

    # Buttons
    btn_instruction = tk.Button(frm_service, text="Instruction", command=lambda: write_instruction(txt_console))
    btn_data_encode = tk.Button(frm_service, text="Encode", command=lambda: encode_data(ent_data_encoded, ent_data_to_encode, txt_console))
    btn_data_decode = tk.Button(frm_service, text="Decode", command=lambda: decode_data(ent_data_decoded, ent_data_to_decode, txt_console))
    btn_data_copy_to_decode = tk.Button(frm_service, text="Copy to Decode", command=lambda: copy_result(ent_data_encoded, ent_data_to_decode))
    btn_clear_encode = tk.Button(frm_service, text="Clear data to encode", command=lambda: clear_data(ent_data_to_encode))
    btn_clear_decode = tk.Button(frm_service, text="Clear data to decode", command=lambda: clear_data(ent_data_to_decode))

    # Grid Layout Configuration
    frm_service.columnconfigure(0, weight=1, uniform='a')
    frm_service.rowconfigure(list(range(14)), weight=1, uniform='a') 

    # Grid Placement
    lbl_data_to_encode.grid(row=6, sticky="ew", padx=2, pady=(0, 0))
    ent_data_to_encode.grid(row=7, sticky="ew", padx=2, pady=(0, 30))  
    lbl_data_encoded.grid(row=8, sticky="ew", padx=2, pady=(0, 0))    
    ent_data_encoded.grid(row=9, sticky="ew", padx=2, pady=(0, 30))    
    lbl_data_to_decode.grid(row=10, sticky="ew", padx=2, pady=(0, 0)) 
    ent_data_to_decode.grid(row=11, sticky="ew", padx=2, pady=(0, 30))  
    lbl_data_decoded.grid(row=12, sticky="ew", padx=2, pady=(0, 0))    
    ent_data_decoded.grid(row=13, sticky="ew", padx=2, pady=(0, 30))     

    btn_instruction.grid(row=0, sticky="nesw", padx=2, pady=2)
    btn_data_encode.grid(row=1, sticky="nesw", padx=2, pady=2)
    btn_data_decode.grid(row=2, sticky="nesw",padx=2, pady=2)
    btn_data_copy_to_decode.grid(row=3, sticky="nesw", padx=2, pady=2)
    btn_clear_encode.grid(row=4, sticky="nesw", padx=2, pady=2)
    btn_clear_decode.grid(row=5, sticky="nesw", padx=2, pady=2)
"""