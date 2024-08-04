import os
import PyPDF2
from tkinter import Tk, filedialog, Button, Label, Entry, StringVar, Listbox, Scrollbar, END, Frame, RIGHT, Y, NW
from tkinter import ttk
from tkinter import PhotoImage

def merge_pdfs(pdf_list, output):
    pdf_merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        pdf_merger.append(pdf)
    with open(output, 'wb') as f:
        pdf_merger.write(f)

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

# Create the main window
root = Tk()
root.title("PDF Merger")

# Set window icon
root.iconphoto(False, PhotoImage(file='pdf_icon.png'))

# Setting the style
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TListbox", font=("Helvetica", 12))

pdf_files = []

# StringVar to update the file list dynamically
file_list_var = StringVar()
output_name_var = StringVar()

# Main frame
main_frame = Frame(root, padx=10, pady=10)
main_frame.pack(fill='both', expand=True)

# Load and place the icon
icon_image = PhotoImage(file='pdf_icon.png')
icon_label = Label(main_frame, image=icon_image)
icon_label.grid(row=0, column=0, columnspan=2, pady=10)

# Widgets
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

# Run the main loop
root.mainloop()
