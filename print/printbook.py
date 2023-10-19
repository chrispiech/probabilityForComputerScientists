import hjson
import PyPDF2
import pdfgenerator
import re
import os
 
# def create_pdfs():
# Opening JSON file
f = open("../bookOutline.hjson")
# returns JSON object as a dictionary
data = hjson.load(f)
# Closing file
f.close()

# folder to store pdfs 
if not os.path.exists('pdfs'):
    os.mkdir('pdfs')

# base url for all pages 
base = 'https://chrispiech.github.io/probabilityForComputerScientists/en/'

# get pdf for title page
pdf_link = base + 'index.html'
title_name = 'titlepage.pdf'
if (not os.path.exists(os.path.join('pdfs', title_name))):
    # generate pdf file
    pdf_file = classprint.PdfGenerator([pdf_link]).main()
    # save pdf to file
    with open(os.path.join('pdfs', title_name), "wb") as outfile:
        outfile.write(pdf_file[0].getbuffer())

# get pdf_name and pdf_link for book from bookOutline and store in pdf_files
pdf_files = {}
count = 0 
for part in data:
    pdf_files[part] = {'sections':{}}
    for page in data[part]['sections']:
        title = data[part]['sections'][page]
        pdf_name = page + '.pdf'
        pdf_link = base + part + '/' + page 
        # store pdf_name and title
        pdf_files[part]['sections'][pdf_name] = title
        # check if pdf already exists
        if (not os.path.exists(os.path.join('pdfs', pdf_name))):
            # generate pdf file
            pdf_file = classprint.PdfGenerator([pdf_link]).main()
            # save pdf to file
            with open(os.path.join('pdfs', pdf_name), "wb") as outfile:
                outfile.write(pdf_file[0].getbuffer())
    if 'examples' in data[part].keys():
        pdf_files[part]['examples'] = {}
        for page in data[part]['examples']:
            title = data[part]['examples'][page]
            pdf_name = page + '.pdf'
            pdf_link = base + 'examples' + '/' + page 
            # store pdf_name and title
            pdf_files[part]['examples'][pdf_name] = title
            # check if pdf already exists
            if (not os.path.exists(os.path.join('pdfs', pdf_name))):
                # generate pdf file
                pdf_file = classprint.PdfGenerator([pdf_link]).main()
                # save pdf to file
                with open(os.path.join('pdfs', pdf_name), "wb") as outfile:
                    outfile.write(pdf_file[0].getbuffer())
    count+=1
    if count==2:
        break
# Output PDF file name
output_pdf = "CS109Book.pdf"

# Create a PDF file writer object
pdf_writer = PyPDF2.PdfWriter()

# add title page
pdf_writer.append(os.path.join('pdfs', title_name))

page_num = 1 
for part in pdf_files:
    title = data[part]['title']
    if title is None:
        title = "Introduction"
    # create outline for parts
    part_outline = pdf_writer.add_outline_item(title, page_num)
    # add pdf files to table of contents and book
    for pdf_file, title in pdf_files[part]['sections'].items():
        # Open the pdf
        pdf_reader = PyPDF2.PdfReader(open(os.path.join('pdfs', pdf_file), "rb"))
        # Create an outline item for the pdf
        pdf_outline = pdf_writer.add_outline_item(title, page_num, parent=part_outline)
        # add pdf file to book pdf 
        pdf_writer.append(os.path.join('pdfs', pdf_file))
        # start of next pdf 
        page_num += len(pdf_reader.pages)
    if 'examples' in pdf_files[part].keys():
        # create outline for examples
        examples_outline = pdf_writer.add_outline_item('Applications', page_num, parent=part_outline)
        # add pdf files to table of contents and book
        for pdf_file, title in pdf_files[part]['examples'].items():
            # Open the pdf
            pdf_reader = PyPDF2.PdfReader(open(os.path.join('pdfs', pdf_file), "rb"))
            # Create an outline item for the pdf
            pdf_outline = pdf_writer.add_outline_item(title, page_num, parent=examples_outline)
            pdf_writer.append(os.path.join('pdfs', pdf_file))
            # start of next pdf 
            page_num += len(pdf_reader.pages)

# Save the merged PDF with the TOC
with open(output_pdf, "wb") as output_file:
    pdf_writer.write(output_file)

print(f"Merged PDF with Table of Contents saved as {output_pdf}")