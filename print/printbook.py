import hjson
import json
import PyPDF2
import pdfgenerator
import re
import os
from tqdm import tqdm
import hashlib
import subprocess
import socket
import time

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


"""
Before you run this script, you should host a local http server on port 8000.
You can do that by running the script ./runLocal in the root directory
"""

TO_SKIP = {
    "calculators": True,
}
PORT = 8000

# returns JSON object as a dictionary
data = hjson.load(open("../bookOutline.hjson"))


# get pdf_name and pdf_link for book from bookOutline and store in pdf_files
pdf_files = {}

# folder to store pdfs 
if not os.path.exists('pdfs'):
    os.mkdir('pdfs')

# load the hash values
# if the file does not exist, hash_values is {}
if not os.path.exists('hash_values.json'):
    hash_values = {}
else:
    hash_values = json.load(open('hash_values.json', 'r'))



# base url for all pages 
base = f'http://localhost:{PORT}/en/'


def print_title_page():
    # get pdf for title page
    pdf_link = base + 'index.html'
    title_name = 'titlepage.pdf'

    file_link = f'../en/index.html'
    raw_file_html = open(file_link, 'r').read()
    hash = compute_md5(raw_file_html)
    if file_link in hash_values.keys() and hash_values[file_link] == hash:
        return
    print('printing title page...')

    # generate pdf file
    pdf_file = pdfgenerator.PdfGenerator([pdf_link]).main()
    # save pdf to file
    with open(os.path.join('pdfs', title_name), "wb") as outfile:
        outfile.write(pdf_file[0].getbuffer())
        save_hash_value(hash, file_link)

def print_page(part, page):
    pdf_name = page + '.pdf'
    pdf_link = base + part + '/' + page
    file_link = f'../en/{part}/{page}/index.html'
    raw_file_html = open(file_link, 'r').read()
    hash = compute_md5(raw_file_html)
    if file_link in hash_values.keys() and hash_values[file_link] == hash:
        return
    # store pdf_name and title
    # generate pdf file
    print(f'Making {part}/{page}')
    pdf_file = pdfgenerator.PdfGenerator([pdf_link]).main()
    # save pdf to file
    with open(os.path.join('pdfs', pdf_name), "wb") as outfile:
        outfile.write(pdf_file[0].getbuffer())
        save_hash_value(hash, file_link)

def save_to_contents(part, page_type, page):
    # save for table of contents
    title = data[part][page_type][page]
    pdf_name = page + '.pdf'
    pdf_files[part][page_type][pdf_name] = title

def is_special_case(page):
    if page in TO_SKIP:
        return True
    return False

def handle_special_case(part, page):
    if page in TO_SKIP:
        return

def handle_random_variable_ref():
    print('handling random variable ref')

def print_each_page():
    print_title_page()
    for part in data:
        print(f'Printing pages in section {part}...')
        pdf_files[part] = {'sections':{}}
        for page in data[part]['sections']:
            if is_special_case(page):
                handle_special_case(part, page)
                continue
            print_page(part, page)
            save_to_contents(part, 'sections', page)
            
        if 'examples' in data[part].keys():
            pdf_files[part]['examples'] = {}
            for page in data[part]['examples']:
                print_page('examples', page)
                # save for table of contents
                save_to_contents(part, 'examples', page)

def print_book():
    # first, start a local http server (python3 -m http.server) from this python script
    wait_for_server(PORT)

    print('Printing book...')

    # print all sections
    print_each_page()

    # create the final PDF
    merge_pdfs()

def merge_pdfs():
    print('Merging PDFs...')
    # Output PDF file name
    output_pdf = "../en/ProbabilityForComputerScientists.pdf"

    # Create a PDF file writer object
    pdf_writer = PyPDF2.PdfWriter()

    # add title page
    with open(os.path.join('pdfs', 'titlepage.pdf'), 'rb') as f:
        pdf_writer.add_page(PyPDF2.PdfReader(f).pages[0])
    pdf_writer.add_outline_item('Title Page', 0)

    page_num = 1
    for part in pdf_files:
        title = data[part]['title'] if data[part]['title'] else "Introduction"


        # create outline for parts
        part_outline = pdf_writer.add_outline_item(title, page_num)

        # Create and add the separator page
        separator_filename = os.path.join('pdfs', f'separator_{part}.pdf')
        create_separator(f"{title}", separator_filename)
        
        with open(separator_filename, 'rb') as f:
            separator_reader = PyPDF2.PdfReader(f)
            pdf_writer.add_page(separator_reader.pages[0])
        pdf_writer.add_outline_item(title, page_num, parent=part_outline)
        page_num += 1
        

        # add pdf files to table of contents and book
        for pdf_file, title in pdf_files[part]['sections'].items():
            # Open the pdf
            with open(os.path.join('pdfs', pdf_file), "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
                # Create an outline item for the pdf
                pdf_writer.add_outline_item(title, page_num, parent=part_outline)
                # start of next pdf 
                page_num += len(pdf_reader.pages)
        if 'examples' in pdf_files[part].keys():
            # create outline for examples
            examples_outline = pdf_writer.add_outline_item('Applications', page_num, parent=part_outline)
            # add pdf files to table of contents and book
            for pdf_file, title in pdf_files[part]['examples'].items():
                # Open the pdf
                with open(os.path.join('pdfs', pdf_file), "rb") as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
                    # Create an outline item for the pdf
                    pdf_writer.add_outline_item(title, page_num, parent=examples_outline)
                    # start of next pdf 
                    page_num += len(pdf_reader.pages)

    # Add Meta Data
    metadata = {
        '/Title': 'Probability for Computer Scientists: CS109 Course Reader',
        '/Author': 'Chris Piech'
    }
    pdf_writer.add_metadata(metadata)

    # Save the merged PDF with the TOC
    with open(output_pdf, "wb") as output_file:
        pdf_writer.write(output_file)

    print(f"Merged PDF saved as {output_pdf}")

def save_hash_value(hash, file_link):

    # store the hash value
    hash_values[file_link] = hash

    # save the hash values to json
    with open('hash_values.json', 'w') as fp:
        json.dump(hash_values, fp, indent=4)

def compute_md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()

# def run_http_server(port=8000):
#     cmd = ['python3', '-m', 'http.server', str(port)]
#     subprocess.Popen(cmd)
#     wait_for_server(port)

def wait_for_server(port=8000, timeout=10):
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            raise TimeoutError("Unable to connect to the server within timeout.")
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(('127.0.0.1', port))
            return  # Server is up and connection is successful
        except ConnectionRefusedError:
            pass  # Server not yet up
        finally:
            s.close()
        
        time.sleep(0.1)

def create_separator(text, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Times-Bold", 36)  # Setting font type and size
    c.drawCentredString(width / 2, height / 2, text)  # Centering the text on the page
    c.save()

if __name__ == "__main__":
    print_book()