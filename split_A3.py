import sys
import os
from pypdf import PdfWriter, PdfReader

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

title = input("Please enter the title of the piece: ")

for x, filename in enumerate(pdfFiles):
    #Open the file to read
    with open(filename, "rb") as score:
        score_in = PdfReader(score)
        score_out = PdfWriter()
        print("\nNow processing: " + filename)

        #Get number of pages in file
        numPages = len(score_in.pages)

        #Get current file dimensions
        page = score_in.pages[0]
        page_x, page_y = page.cropbox.upper_right

        for i in range(numPages):
            page = score_in.pages[i]
            #Crop left side
            page.mediabox.upper_right = (page_x, page_y)
            page.mediabox.lower_left = (0, page_y/2)
            score_out.add_page(page)
            #Crop right side
            page.mediabox.upper_right = (page_x, page_y/2)
            page.mediabox.lower_left = (0, 0)
            score_out.add_page(page)
        #Create new directory for first file
        if not x:
            try:
                current_dir = os.getcwd()
                new_dir = title + "_cropped"
                new_path = os.path.join(current_dir, new_dir)
                if not os.path.isdir(new_path):
                    os.mkdir(new_path)
                new_path += "/"
            except:
                print("There was an error creating the new directory: " + new_path)

        #Write cropped pages to new file in new directory
        try:
            index = x
            while os.path.isfile(new_path + title + str(index) + ".pdf"):
                index += 1
            with open(new_path + title + str(index) + ".pdf", "wb") as score:
                score_out.write(score)
        except:
            print("There was an error writing the file.")

print("\nDone processing " + title)