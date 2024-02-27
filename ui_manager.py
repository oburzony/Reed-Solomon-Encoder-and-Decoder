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
    frm_service = tk.Frame(root, bg="white", bd=2, relief=tk.RAISED)
    frm_service.pack(fill=tk.Y, side=tk.LEFT)

    frm_console = tk.Frame(root, bg="black")
    frm_console.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    frm_buttons = tk.Frame(frm_service, bg="lightgray")
    frm_buttons.pack(fill=tk.X)

    frm_labels_entries = tk.Frame(frm_service, bg="lightgray")
    frm_labels_entries.pack(fill=tk.BOTH, expand=True)

    frm_encode = tk.Frame(frm_labels_entries, bg="lightgray")
    frm_encode.grid(row=0, sticky="ew", padx=5, pady=5)

    frm_encoded = tk.Frame(frm_labels_entries, bg="lightgray")
    frm_encoded.grid(row=1, sticky="ew", padx=5, pady=5)

    frm_decode = tk.Frame(frm_labels_entries, bg="lightgray")
    frm_decode.grid(row=2, sticky="ew", padx=5, pady=5)

    frm_decoded = tk.Frame(frm_labels_entries, bg="lightgray")
    frm_decoded.grid(row=3, sticky="ew", padx=5, pady=5)

    # Texts 
    txt_console = tk.Text(frm_console, bg="black", fg="white")
    txt_console.pack(fill=tk.BOTH, expand=True)

    # Grid Layout Configuration
    frm_service.columnconfigure(0, weight=1)
    frm_service.rowconfigure([0, 1], weight=1, uniform='a')
    frm_buttons.columnconfigure(0, weight=1, uniform='a')
    frm_buttons.rowconfigure(list(range(6)), weight=1, uniform='a')
    frm_labels_entries.columnconfigure(0, weight=1, uniform='a')
    frm_labels_entries.rowconfigure(list(range(4)), weight=1, uniform='a')

    # Labels and Entries
    lbl_data_to_encode = tk.Label(frm_encode, text="Enter data to encode (9 numbers [0-15]):", bg="lightgray")  
    lbl_data_encoded = tk.Label(frm_encoded, text="Encoded data:", bg="lightgray")  
    lbl_data_to_decode = tk.Label(frm_decode, text="Enter data to decode (15 numbers [0-15]):", bg="lightgray")  
    lbl_data_decoded = tk.Label(frm_decoded, text="Decoded data:", bg="lightgray")  

    ent_data_to_encode = tk.Entry(frm_encode, validate="key", validatecommand=(frm_service.register(validate_entry_encode), "%P")) 
    ent_data_to_decode = tk.Entry(frm_decode, validate="key", validatecommand=(frm_service.register(validate_entry_decode), "%P"))  

    ent_data_encoded = tk.Entry(frm_encoded, state="readonly") 
    ent_data_decoded = tk.Entry(frm_decoded, state="readonly") 

    # Buttons
    btn_instruction = tk.Button(frm_buttons, text="Instruction", command=lambda: write_instruction(txt_console))
    btn_data_encode = tk.Button(frm_buttons, text="Encode", command=lambda: encode_data(ent_data_encoded, ent_data_to_encode, txt_console))
    btn_data_decode = tk.Button(frm_buttons, text="Decode", command=lambda: decode_data(ent_data_decoded, ent_data_to_decode, txt_console))
    btn_data_copy_to_decode = tk.Button(frm_buttons, text="Copy to Decode", command=lambda: copy_result(ent_data_encoded, ent_data_to_decode))
    btn_clear_encode = tk.Button(frm_buttons, text="Clear data to encode", command=lambda: clear_data(ent_data_to_encode))
    btn_clear_decode = tk.Button(frm_buttons, text="Clear data to decode", command=lambda: clear_data(ent_data_to_decode))

    # Grid Placement
    lbl_data_to_encode.pack(fill=tk.BOTH, expand=True)
    ent_data_to_encode.pack(fill=tk.BOTH, expand=True)

    lbl_data_encoded.pack(fill=tk.BOTH, expand=True)
    ent_data_encoded.pack(fill=tk.BOTH, expand=True)
    
    lbl_data_to_decode.pack(fill=tk.BOTH, expand=True)
    ent_data_to_decode.pack(fill=tk.BOTH, expand=True)
    
    lbl_data_decoded.pack(fill=tk.BOTH, expand=True)
    ent_data_decoded.pack(fill=tk.BOTH, expand=True)

    btn_instruction.grid(row=0, sticky="ew", padx=5, pady=5)
    btn_data_encode.grid(row=1, sticky="ew", padx=5, pady=5)
    btn_data_decode.grid(row=2, sticky="ew", padx=5, pady=5)
    btn_data_copy_to_decode.grid(row=3, sticky="ew", padx=5, pady=5)
    btn_clear_encode.grid(row=4, sticky="ew", padx=5, pady=5)
    btn_clear_decode.grid(row=5, sticky="ew", padx=5, pady=5)




    