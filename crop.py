import sys
import os
from pypdf import PdfWriter, PdfReader

#Definition static variables
pdfFiles = []
#(conversion ratio pts to mm)
points_to_mm = 0.352777778

#Function for entering crop margins
def get_margins():
    #Ask trim right
    while True:
        trim_right = input("How much do you want to trim right (mm): ")
        if trim_right.isdigit():
            trim_right = int(trim_right)
            break
        else:
            print(trim_right + " is not a valid value.")

    #Ask trim left
    while True:
        trim_left = input("How much do you want to trim left (mm): ")
        if trim_left.isdigit():
            trim_left = int(trim_left)
            break
        else:
            print(trim_left + " is not a valid value.")
    
    #Ask trim top
    while True:
        trim_top = input("How much do you want to trim from the top (mm): ")
        if trim_top.isdigit():
            trim_top = int(trim_top)
            break
        else:
            print(trim_top + " is not a valid value.")
    
    #Ask trim bottom
    while True:
        trim_bottom = input("How much do you want to trim from the bottom (mm): ")
        if trim_bottom.isdigit():
            trim_bottom = int(trim_bottom)
            break
        else:
            print(trim_bottom + " is not a valid value.")
            break
    return(trim_right,trim_left,trim_top,trim_bottom)

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

        #Show current file dimensions
        page = score_in.pages[0]
        page_x, page_y = page.cropbox.upper_right
        #Convert points to mm
        page_x = round(float(page_x) * points_to_mm)
        page_y = round(float(page_y) * points_to_mm)
        print("Page size: " + str(page_x) + "x" + str(page_y))

        #Give user the option to keep previous margins
        if x:
            while True:
                answer = input("\nWould you like to keep the previous crop margins? (y/n): ")
                if (answer == 'n' or answer ==  'N') and answer != 'y' and answer != 'Y':
                    trim_right, trim_left, trim_top, trim_bottom = get_margins()
                    break
                elif answer != 'n' and answer != 'N' and answer != 'y' and answer != 'Y':
                    print("Please enter 'y' or 'n'.")
                else:
                    break
        else:
            trim_right, trim_left, trim_top, trim_bottom = get_margins()

        #Crop all pages
        for i in range(numPages):
            page = score_in.pages[i]
            print("New top-right coordinate: (" + str(page_x-trim_right) + ";" + str(page_y-trim_top) + ")")
            print("New bottom-left coordinate: (" + str(trim_left) + ";" + str(trim_bottom) + ")")
            #Crop the file
            page.mediabox.upper_right = ((page_x-trim_right)/points_to_mm, (page_y-trim_top)/points_to_mm)
            page.mediabox.lower_left = (trim_left/points_to_mm, trim_bottom/points_to_mm)
            score_out.add_page(page)

    #Create new directory for first file
    if not x:
        try:
            current_dir = os.getcwd()
            new_dir = title + "_cropped"
            new_path = os.path.join(current_dir, new_dir)
            os.mkdir(new_path)
            new_path += "/"
        except:
            print("There was an error creating the new directory: " + new_path)

    #Write cropped pages to new file in new directory
    try:
        with open(new_path + title + str(x) + ".pdf", "wb") as score:
            score_out.write(score)
    except:
        print("There was an error writing the file.")

print("\nDone processing " + title)