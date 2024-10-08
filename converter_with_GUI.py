import os
import PyPDF2
from tkinter import Tk, filedialog, Button, Label, Entry, StringVar, Listbox, Scrollbar, END, Frame, RIGHT, Y
from tkinter import ttk
from tkinter import PhotoImage

def merge_pdfs(pdf_list, output):
    pdf_merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        pdf_merger.append(pdf)
    with open(output, 'wb') as f:
        pdf_merger.write(f)

def convert_pdf_to_txt(pdf_path):
    base_name = os.path.splitext(pdf_path)[0]
    txt_file_name = f"{base_name}_converted.txt"
    
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
                
                # Add additional formatting if it's not the last page
                if page_num < len(reader.pages) - 1:
                    text += "\n\n--------------\n"
                    text += f"This is page {page_num + 1}\n"
        
        with open(txt_file_name, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
        
        return f"Text successfully extracted to {txt_file_name}"
    
    except FileNotFoundError:
        return f"Error: The file {pdf_path} does not exist."
    except Exception as e:
        return f"An error occurred: {e}"

def open_merge_window():
    main_window.destroy()  # Close the main window
    merge_window = Tk()
    merge_window.title("PDF Merger")

    # Set window icon
    merge_window.iconphoto(False, PhotoImage(file='pdf_icon.png'))

    # Setting the style
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 12))
    style.configure("TEntry", font=("Helvetica", 12))
    style.configure("TListbox", font=("Helvetica", 12))

    pdf_files = []
    output_name_var = StringVar()

    def add_first_pdf():
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf_files.clear()
            pdf_files.append(file_path)
            update_file_list()

    def add_next_pdf():
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf_files.append(file_path)
            update_file_list()

    def update_file_list():
        listbox.delete(0, END)
        for pdf in pdf_files:
            listbox.insert(END, pdf)

    def create_merged_pdf():
        output_name = output_name_var.get() + '.pdf'
        if pdf_files and output_name:
            merge_pdfs(pdf_files, output_name)
            status_label.config(text=f"PDFs merged successfully into {output_name}.")
        else:
            status_label.config(text="Please add PDFs and specify the output file name.")

    # Main frame
    main_frame = Frame(merge_window, padx=10, pady=10)
    main_frame.pack(fill='both', expand=True)

    # Load and place the icon
    icon_image = PhotoImage(file='pdf_icon.png')
    icon_label = Label(main_frame, image=icon_image)
    icon_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Widgets for merging PDFs
    Label(main_frame, text="Select PDF files to merge:").grid(row=1, column=0, pady=5, sticky='w')

    add_first_button = ttk.Button(main_frame, text="Add First PDF", command=add_first_pdf)
    add_first_button.grid(row=1, column=1, pady=5, sticky='e')

    add_next_button = ttk.Button(main_frame, text="Add Next PDF", command=add_next_pdf)
    add_next_button.grid(row=2, column=1, pady=5, sticky='e')

    Label(main_frame, text="Selected PDF files:").grid(row=3, column=0, pady=5, sticky='w')

    # Listbox with scrollbar
    listbox_frame = Frame(main_frame)
    listbox_frame.grid(row=4, column=0, columnspan=2, pady=5, sticky='nswe')

    scrollbar = Scrollbar(listbox_frame, orient='vertical')
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(listbox_frame, yscrollcommand=scrollbar.set, font=("Helvetica", 12))
    listbox.pack(fill='both', expand=True)

    scrollbar.config(command=listbox.yview)

    Label(main_frame, text="Enter the name of the output PDF file (without .pdf extension):").grid(row=5, column=0, pady=5, sticky='w')

    output_entry = ttk.Entry(main_frame, textvariable=output_name_var)
    output_entry.grid(row=5, column=1, pady=5, sticky='e')

    merge_button = ttk.Button(main_frame, text="Merge PDFs", command=create_merged_pdf)
    merge_button.grid(row=6, column=0, columnspan=2, pady=10)

    status_label = ttk.Label(main_frame, text="")
    status_label.grid(row=7, column=0, columnspan=2, pady=5)

    # Configure column and row weights to ensure resizing
    main_frame.grid_rowconfigure(4, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)

    merge_window.mainloop()

def open_convert_window():
    main_window.destroy()  # Close the main window
    convert_window = Tk()
    convert_window.title("PDF to Text Converter")

    # Set window icon
    convert_window.iconphoto(False, PhotoImage(file='pdf_icon.png'))

    # Setting the style
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 12))
    style.configure("TEntry", font=("Helvetica", 12))

    pdf_files = []

    def add_pdf():
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf_files.clear()
            pdf_files.append(file_path)
            status_label.config(text="PDF file selected for conversion.")

    def convert_selected_pdf():
        if pdf_files:
            selected_file = pdf_files[0]  # Just use the first file for conversion
            result = convert_pdf_to_txt(selected_file)
            status_label.config(text=result)
        else:
            status_label.config(text="Please add a PDF file to convert.")

    # Main frame
    main_frame = Frame(convert_window, padx=10, pady=10)
    main_frame.pack(fill='both', expand=True)

    # Load and place the icon
    icon_image = PhotoImage(file='pdf_icon.png')
    icon_label = Label(main_frame, image=icon_image)
    icon_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Widgets for converting PDF to text
    Label(main_frame, text="Select a PDF file to convert to text:").grid(row=1, column=0, pady=5, sticky='w')

    add_button = ttk.Button(main_frame, text="Add PDF", command=add_pdf)
    add_button.grid(row=1, column=1, pady=5, sticky='e')

    convert_button = ttk.Button(main_frame, text="Convert Selected PDF to TXT", command=convert_selected_pdf)
    convert_button.grid(row=2, column=0, columnspan=2, pady=10)

    status_label = ttk.Label(main_frame, text="")
    status_label.grid(row=3, column=0, columnspan=2, pady=5)

    # Configure column and row weights to ensure resizing
    main_frame.grid_rowconfigure(2, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)

    convert_window.mainloop()

# Create the main window
main_window = Tk()
main_window.title("PDF Tools")

# Set window icon
main_window.iconphoto(False, PhotoImage(file='pdf_icon.png'))

# Setting the style
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))

# Main frame
main_frame = Frame(main_window, padx=10, pady=10)
main_frame.pack(fill='both', expand=True)

# Load and place the icon
icon_image = PhotoImage(file='pdf_icon.png')
icon_label = Label(main_frame, image=icon_image)
icon_label.grid(row=0, column=0, columnspan=2, pady=10)

# Widgets for main window
Label(main_frame, text="Select an action:").grid(row=1, column=0, pady=5, sticky='w')

merge_button = ttk.Button(main_frame, text="Merge PDFs", command=open_merge_window)
merge_button.grid(row=1, column=1, pady=5, sticky='e')

convert_button = ttk.Button(main_frame, text="Convert PDF to TXT", command=open_convert_window)
convert_button.grid(row=2, column=1, pady=5, sticky='e')

# Configure column and row weights to ensure resizing
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# Run the main loop
main_window.mainloop()
