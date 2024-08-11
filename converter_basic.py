import os
import PyPDF2

def merge_pdfs(pdf_list, output):
    pdf_merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        pdf_merger.append(pdf)
    with open(output, 'wb') as f:
        pdf_merger.write(f)
    print(f"PDFs merged successfully into {output}.")

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
        
        print(f"Text successfully extracted to {txt_file_name}")
    
    except FileNotFoundError:
        print(f"Error: The file {pdf_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def list_pdfs(directory):
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    pdf_files.sort()  # Optional: Sort the files alphabetically
    return pdf_files

def display_files(files):
    print("Available PDF files:")
    for index, file in enumerate(files):
        print(f"{index + 1}: {file}")

def get_selected_files(files):
    while True:
        indices = input("Enter the indices of the PDF files to merge, separated by commas (e.g., 2,1): ").strip()
        try:
            indices = [int(i.strip()) - 1 for i in indices.split(',')]
            if all(0 <= i < len(files) for i in indices):
                return [files[i] for i in indices]
            else:
                print("One or more indices are out of range. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")

def get_selected_file(files):
    while True:
        index = input("Enter the index of the PDF file you want to convert to TXT: ").strip()
        try:
            index = int(index) - 1
            if 0 <= index < len(files):
                return files[index]
            else:
                print("Index out of range. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_output_filename():
    output_name = input("Enter the name of the output PDF file (without .pdf extension): ")
    return output_name + '.pdf'

def main():
    directory = os.path.dirname(os.path.abspath(__file__))

    pdf_files = list_pdfs(directory)
    if not pdf_files:
        print("No PDF files found in the current directory. Exiting.")
        return

    print("Choose an action:")
    print("1: Merge PDFs")
    print("2: Convert a PDF to Text File")
    
    choice = input("Enter the number corresponding to your choice: ")
    
    if choice == '1':
        display_files(pdf_files)
        selected_files = get_selected_files(pdf_files)
        if not selected_files:
            print("No files selected. Exiting.")
            return
        
        output_filename = get_output_filename()
        full_paths = [os.path.join(directory, file) for file in selected_files]
        merge_pdfs(full_paths, output_filename)
        
    elif choice == '2':
        display_files(pdf_files)
        selected_file = get_selected_file(pdf_files)
        if not selected_file:
            print("No file selected. Exiting.")
            return
        
        full_path = os.path.join(directory, selected_file)
        convert_pdf_to_txt(full_path)
    
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
