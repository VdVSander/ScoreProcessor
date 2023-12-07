import sys
import os
from pypdf import PdfWriter, PdfReader
import pdf2image
from PIL import Image
import PIL

def check_input(arg):
    pdfFiles = []
    #Check the entered arguments
    try:
        #Show the manual
        if arg == "--man" or arg == "-m" or arg == "m" or arg == "manual":
            print("Usage: python3 crop.py <path> or [--all/-a] for all files in the current directory")
            sys.exit()
        #Get all PDF files from the current working directory
        elif arg == "--all" or arg == "-a":
            dir_content = os.listdir()
            for file in dir_content:
                if file[-4:] == ".pdf" and os.path.isfile(file):
                    pdfFiles.append(file)
            if not pdfFiles:
                print("No PDF files were found in this directory")
            else:
                print("We found " + str(len(pdfFiles)) + " PDF file(s).")
        #Get the PDF file from the path
        elif os.path.isfile(arg) and arg[-4:] == ".pdf":
            pdfFiles.append(arg)
        else:
            print("Please enter a valid path to a PDF file or use the --man argument for more information.")
            sys.exit()
    except:
        print("Please enter a valid path to a PDF file or use the --man argument for more information.")
        sys.exit()
    return pdfFiles

def check_temp_dir():
    dir_name = "temp"
    # Check if the directory already exists
    if not os.path.exists(dir_name):
        # If it doesn't exist, create it
        os.makedirs(dir_name)

def pdf_to_png(pdfFiles):
    #Repeat for every PDF file
    for x, filename in enumerate(pdfFiles):
        print(filename)
        #Convert the PDF file to images of every page
        images = pdf2image.convert_from_path(filename)
        #Save every page in the temporary directory
        for i in range(len(images)):
            print("Page " + str(i+1) + " / " + str(len(images)))
            images[i].save('temp/page'+str(i)+'.png', 'PNG')
        #Clear the list again for the next PDF file
        images = []
        #
        for path in os.listdir("temp/"):
            if os.path.isfile(os.path.join("temp/", path)):
                images.append(os.path.join("temp/", path))
    return(images)

def rotate_image(im, degrees):
    im = im.rotate(degrees, PIL.Image.NEAREST, expand = 1)
    im.show()
    answer = input("OK? (y/n): ")
    im.save(image)
    return(im, answer)

def png_to_pdf():
    #Open the images and then convert them back to PDF
    open_images = [Image.open(image_path) for image_path in images]
    converted_images = [image.convert('RGB') for image in open_images]
    return(converted_images)

def save_pdf_files(converted_images):
    #Save the PDF files
    title = input("Please enter the title of the piece: ")
    converted_images[0].save("./" + title + ".pdf", save_all=True, append_images=converted_images)

def remove_temp_files():
    # Get a list of all files in the temporary directory
    file_list = os.listdir("./temp/")

    # Iterate through the files and remove them
    for file_name in file_list:
        file_path = os.path.join("./temp/", file_name)
        
        # Check if the path is a file (not a directory)
        if os.path.isfile(file_path):
            os.remove(file_path)

# -- MAIN PROGRAM -- #

pdfFiles = check_input(sys.argv[1])
check_temp_dir()
images = pdf_to_png(pdfFiles)

#Iterate over every page and rotate it until it's as desired
for image in images:
    #Show the image of the page
    im = Image.open(image)
    im.show()
    answer = 'n'
    while answer != 'y':
        degrees = input("How many degrees would you like to rotate this image: ")
        print("Please close the previous window.")
        if(degrees == "l"):
            degrees = 90
            im, answer = rotate_image(im, degrees)
        elif(degrees == "r"):
            degrees = -90
            im, answer = rotate_image(im, degrees)
        elif(degrees.isnumeric()):
            degrees = int(degrees)
            im, answer = rotate_image(im, degrees)
        else:
            print("Please enter a valid response (l,r or °)")
            answer = "n"

save_pdf_files(png_to_pdf())
remove_temp_files()