import os
import PyPDF2

def merge_pdfs(pdf_list, output):
    pdf_merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        pdf_merger.append(pdf)
    with open(output, 'wb') as f:
        pdf_merger.write(f)

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
        indices = input("Enter the indices of the PDF files to merge, separated by commas (e.g., 2,1): ")
        try:
            indices = [int(i.strip()) - 1 for i in indices.split(',')]
            if all(0 <= i < len(files) for i in indices):
                return [files[i] for i in indices]
            else:
                print("One or more indices are out of range. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")

def get_output_filename():
    # Prompt the user to enter the output filename
    output_name = input("Enter the name of the output PDF file (without .pdf extension): ")
    return output_name + '.pdf'

def main():
    # Directory is the same as the script's location
    directory = os.path.dirname(os.path.abspath(__file__))

    # List PDF files in the same directory as the script
    pdf_files = list_pdfs(directory)
    if not pdf_files:
        print("No PDF files found in the current directory. Exiting.")
        return

    # Display the list of PDF files
    display_files(pdf_files)

    # Get the user-selected files in the specified order
    selected_files = get_selected_files(pdf_files)
    
    if not selected_files:
        print("No files selected. Exiting.")
        return

    # Get the output filename
    output_filename = get_output_filename()

    # Merge PDFs
    full_paths = [os.path.join(directory, file) for file in selected_files]
    merge_pdfs(full_paths, output_filename)
    print(f"PDFs merged successfully into {output_filename}.")

if __name__ == "__main__":
    main()