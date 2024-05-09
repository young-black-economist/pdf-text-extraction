## Import libraries ##
# Read pdfs
from PyPDF2 import PdfWriter, PdfReader
# Analyze
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTFigure
# Extract images
from PIL import Image
from pdf2image import convert_from_path
# OCR
import pytesseract 
# Remove extra files
import os
import json

# Crop the image in the PDF files
def cut_pix(bite, canvas):
    # Find coordinates to of images
    [pix_left, pix_top, pix_right, pix_bottom] = [bite.x0,bite.y0,bite.x1,bite.y1] 
    # Crop the coordinates
    canvas.mediabox.lower_left = (pix_left, pix_bottom)
    canvas.mediabox.upper_right = (pix_right, pix_top)
    # Put cropped image on new PDF
    cut_writer = PdfWriter()
    cut_writer.add_page(canvas)
    # Save this to a new file
    with open('cut_pix.pdf', 'wb') as cut_pdf_file:
        cut_writer.write(cut_pdf_file)

# Change PDF to PNGs
def pdf2png(in_file,):
    pixs = convert_from_path(in_file, poppler_path=r'C:\Release-23.11.0-0\poppler-23.11.0\Library\bin')
    pix = pixs[0]
    out_file = 'PDF_pix.png'
    pix.save(out_file, 'PNG')

# Use OCR to decipher text
def png2text(pix_path):
    img = Image.open(pix_path)
    # Extract text
    text = pytesseract.image_to_string(img)
    return text

# Find the PDF
pdf_location = 'B-TV-BC-YB-2003-04_5-7.pdf'
# Create pdf file and reader objects
pdf_attach = open(pdf_location, 'rb')
pdfread = PdfReader(pdf_attach)

# Create the dictionary to extract text from each image
text_in_canvas = {}

# Extract the pages from the PDF
for scroll_num, scroll in enumerate(extract_pages(pdf_location)):

    # Create variables
    canvas = pdfread.pages[scroll_num]
    scroll_text = []
    line_format = []
    text_in_pixs = []
    scroll_content = []
    
    # Find all the elements
    scroll_bite = [(bite.y1, bite) for bite in scroll._objs]
    # Sort
    scroll_bite.sort(key=lambda a: a[0], reverse=True)


    # Find elements in a page
    for i,component in enumerate(scroll_bite):
        # Extract
        bite = component[1]
        # Loop through pages
        if isinstance(bite, LTFigure):
                # Use function to crop the image from PDF
            cut_pix(bite, canvas)
                # Use function to convert the pdf to image
            pdf2png('cut_pix.pdf')
                # Use function to pull text from image
            pix_text = png2text('PDF_pix.png')
            text_in_pixs.append(pix_text)
            scroll_content.append(pix_text)
                # Add a placeholder in the text and format lists
            scroll_text.append('pix')
            line_format.append('pix')
                # Update the flag for image detection
          


# Create dictionary key
dctkey = 'Page_'+str(scroll_num)
# Add the list to keys
text_in_canvas[dctkey]= [scroll_text, line_format, text_in_pixs, scroll_content]

# Close the pdf file object
pdf_attach.close()

# Remove extra files
os.remove('cut_pix.pdf')
os.remove('PDF_pix.png')

result = ''.join(text_in_canvas['Page_0'][3])
print(result)


