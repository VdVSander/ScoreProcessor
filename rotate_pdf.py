import sys
import os
from pypdf import PdfWriter, PdfReader
import pdf2image
from PIL import Image
import PIL

#Definition static variables
pdfFiles = []

#Check the entered arguments
try:
    #Show the manual
    if sys.argv[1] == "--man" or sys.argv[1] == "-m" or sys.argv[1] == "m" or sys.argv[1] == "manual":
        print("Usage: python3 crop.py <path> or [--all/-a] for all files in the current directory")
        sys.exit()
    #Get all PDF files from the current working directory
    elif sys.argv[1] == "--all" or sys.argv[1] == "-a":
        dir_content = os.listdir()
        for file in dir_content:
            if file[-4:] == ".pdf" and os.path.isfile(file):
                pdfFiles.append(file)
        if not pdfFiles:
            print("No PDF files were found in this directory")
        else:
            print("We found " + str(len(pdfFiles)) + " PDF file(s).")
    #Get the PDF file from the path
    elif os.path.isfile(sys.argv[1]) and sys.argv[1][-4:] == ".pdf":
        pdfFiles.append(sys.argv[1])
    else:
        print("Please enter a valid path to a PDF file or use the --man argument for more information.")
        sys.exit()
except:
    print("Please enter a valid path to a PDF file or use the --man argument for more information.")
    sys.exit()

dir_name = "temp"
# Check if the directory already exists
if not os.path.exists(dir_name):
    # If it doesn't exist, create it
    os.makedirs(dir_name)

for x, filename in enumerate(pdfFiles):
    #Open the file to read
    images = pdf2image.convert_from_path(filename)
    for i in range(len(images)):
        print("Page " + str(i+1) + " / " + str(len(images)))
        images[i].save('temp/page'+str(i)+'.png', 'PNG')
    images = []
    for path in os.listdir("temp/"):
        if os.path.isfile(os.path.join("temp/", path)):
            images.append(path)
image_paths = []

for image in images:
    im = Image.open("./temp/" + image)
    image_paths.append("./temp/" + image)
    im.show()
    answer = 'n'
    while answer != 'y':
        degrees = input("How many degrees would you like to rotate this image: ")
        print("Please close the previous window.")
        if(degrees == "l"):
            degrees = 90
            im = im.rotate(degrees, PIL.Image.NEAREST, expand = 1)
            im.show()
            answer = input("OK? (y/n): ")
            im.save("./temp/" + image)
        elif(degrees == "r"):
            degrees = -90
            im = im.rotate(degrees, PIL.Image.NEAREST, expand = 1)
            im.show()
            answer = input("OK? (y/n): ")
            im.save("./temp/" + image)
        elif(degrees.isnumeric()):
            degrees = int(degrees)
            im = im.rotate(degrees, PIL.Image.NEAREST, expand = 1)
            im.show()
            answer = input("OK? (y/n): ")
            im.save("./temp/" + image)
        else:
            print("Please enter a valid response (l,r or °)")
            answer = "n"
            

open_images = []
for image_path in image_paths:
    opened_image = Image.open(image_path)
    open_images.append(opened_image)

converted_images = []
for image in open_images:
    converted_image = image.convert('RGB')
    converted_images.append(converted_image)

title = input("Please enter the title of the piece: ")
converted_images[0].save("./" + title + ".pdf", save_all=True, append_images=converted_images)

# Get a list of all files in the temporary directory
file_list = os.listdir("./temp/")

# Iterate through the files and remove them
for file_name in file_list:
    file_path = os.path.join("./temp/", file_name)
    
    # Check if the path is a file (not a directory)
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Removed file: {file_name}")
