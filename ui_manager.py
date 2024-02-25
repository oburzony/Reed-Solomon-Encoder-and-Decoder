import tkinter as tk

def validate_entry_encode(text):
    return text.isdigit() and len(text) <= 9 or text == ""

def validate_entry_decode(text):
    return text.isdigit() and len(text) <= 15 or text == ""


def copy_result(ent_data_encode, ent_data_enter_decode):
    encoded_data = ent_data_encode.get()
    ent_data_enter_decode.config(state="normal") 
    ent_data_enter_decode.delete(0, tk.END) 
    ent_data_enter_decode.insert(0, encoded_data)

def show_result(ent_data):
    ent_data.config(state="normal")  
    ent_data.delete(0, tk.END)     
    ent_data.insert(0, "42")        
    ent_data.config(state="readonly") 

def ui_config(root):
    root.title("Reed-Solomon (15,9) encoder and decoder")
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - window_width)/2)
    center_y = int((screen_height - window_height)/2)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    root.resizable(True, True)

    frm_service = tk.Frame(root, bg="lightgray", bd=2, relief=tk.RAISED)
    frm_service.pack(fill=tk.X)

    for i in range(3):
        frm_service.columnconfigure(i, weight=1, uniform='a')
        frm_service.rowconfigure(i, weight=1, uniform='a')

    lbl_data_to_encode = tk.Label(frm_service, text="Enter data to encode (9 numbers):", bg="lightgray")  
    lbl_data_encoded = tk.Label(frm_service, text="Encoded data:", bg="lightgray")  
    
    lbl_data_to_decode = tk.Label(frm_service, text="Enter data to decode (15 numbers):", bg="lightgray")  
    lbl_data_decoded = tk.Label(frm_service, text="Decoded data:", bg="lightgray")  

    ent_data_to_encode = tk.Entry(frm_service, validate="key", validatecommand=(frm_service.register(validate_entry_encode), "%P"))  
    ent_data_encoded = tk.Entry(frm_service, state="readonly") 

    ent_data_to_decode = tk.Entry(frm_service, validate="key", validatecommand=(frm_service.register(validate_entry_decode), "%P"))  
    ent_data_decoded = tk.Entry(frm_service, state="readonly") 


    btn_data_encode = tk.Button(frm_service, text="Encode", command=lambda: show_result(ent_data_encoded))
    btn_data_decode = tk.Button(frm_service, text="Decode", command=lambda: show_result(ent_data_decoded))
    btn_data_copy_to_decode = tk.Button(frm_service, text="Copy to Decode", command=lambda: copy_result(ent_data_encoded,ent_data_to_decode))

    lbl_data_to_encode.grid(column=0, row=0, sticky="ew", padx=5, pady=5)
    ent_data_to_encode.grid(column=1, row=0, sticky="ew", padx=5, pady=5)
    btn_data_encode.grid(column=2, row=0, sticky="ew", padx=5, pady=5)

    lbl_data_encoded.grid(column=0, row=1, sticky="ew", padx=5, pady=5)
    ent_data_encoded.grid(column=1, row=1, sticky="ew", padx=5, pady=5)
    btn_data_copy_to_decode.grid(column=2, row=1, sticky="ew", padx=5, pady=5)

    lbl_data_to_decode.grid(column=0, row=2, sticky="ew", padx=5, pady=5)
    ent_data_to_decode.grid(column=1, row=2, sticky="ew", padx=5, pady=5)
    btn_data_decode.grid(column=2, row=2, sticky="ew", padx=5, pady=5)

    lbl_data_decoded.grid(column=0, row=3, sticky="ew", padx=5, pady=5)
    ent_data_decoded.grid(column=1, row=3, sticky="ew", columnspan=2, padx=5, pady=5)


    frm_console = tk.Frame(root, bg="black")
    frm_console.pack(fill=tk.BOTH, expand=True, side="bottom")  
    txt_console = tk.Text(frm_console, bg="black", fg="white")
    txt_console.pack(fill=tk.BOTH, expand=True)
