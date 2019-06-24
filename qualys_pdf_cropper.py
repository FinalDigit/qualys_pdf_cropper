#!/usr/bin/python
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import StringIO, os, re, time
from PIL import Image

############################################################################
# Pre-Reqs
# sudo apt install python-pip, pip install Pillow, sudo apt install poppler
############################################################################

path = "pdfs"
print('\n----------------------------------------')
print('[!] Starting Qualys PDF2Image Cropper')
print('----------------------------------------\n')
files = os.listdir('./downloaded_pdfs')

print('[*] Finding .PDF Files')
scan_files = []
for file in files:  # Find All Applicable Scan Files
	#print(file)
	if re.search('.*\.pdf', file) != None:
		print('[*] Found PDF: %s' % file)
		scan_files.append(file)

print('\n')
for file in scan_files:
	print('[*] Current File: %s' % file)
	image = ''
	image = convert_from_path('./downloaded_pdfs/%s' % file, first_page=1, last_page=1, fmt='jpg')
	# Use Output Folder Path for LARGE PDF's
	#image = convert_from_path(file, output_folder=path, first_page=1, last_page=1, fmt='jpg')
	time.sleep(1)
	#image = Image.open(StringIO.StringIO(images))
	w, h = image[0].size
	print('[*] Image Width,Height: %s, %s' % (w,h))
	capture_size_a = ['Report_1', 'Report_2']
	if any(x in file for x in capture_size_a):
		print('[!] Adjustment Needed Found - Changing Capture Size')
		#size = (64, 1080, w-64, h-360)
		size = (64, 1000, w-64, h-420) # 920, 520
	elif 'Report_3' in file.upper():
		print('[!] Adjustment Needed Found - Changing Capture Size: Report_3')
		size = (64, 1080, w-64, h-320) # 1080 # h-360
	else:
		print('[!] Default Capture')
		size = (64, 920, w-64, h-520)
	
	image_region = ''
	image_region = image[0].crop(size)

	# SAVE IMAGES
	image[0].save('./cropped_pdfs/z_%s.png' % file.replace('.pdf',''), 'PNG')  # Save Whole 
	time.sleep(1)
	image_region.thumbnail((720,720))  #  Resize image
	time.sleep(1)
	# Save Cropped Region - PNG, JPG
	image_region.save('./cropped_pdfs/%s_screenshot.png' % file.replace('.pdf',''), 'PNG')  
	print('[*] Finished Processing: %s\n' % file)
	time.sleep(1)
