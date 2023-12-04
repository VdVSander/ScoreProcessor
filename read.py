import sys
import os
import cv2
import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path
from PIL import Image

#Definition static variables
pdfFiles = []
imgFilename = "tempImage.png"
sensitivity = 50

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

for x, filename in enumerate(pdfFiles):
    print("Now processing: " + filename)
    #Convert to image
    pages = convert_from_path(filename, 500)
    for i, page in enumerate(pages):
        if not i:
            page.save(imgFilename, "PNG")
            print("Converted to PNG")
    img = cv2.imread(imgFilename)
    img_height, img_width, trash = img.shape

    data = pytesseract.image_to_data(img, output_type=Output.DICT)
    coordinates = []
    for i in range(len(data["text"])):
        if float(data["conf"][i]) > sensitivity:
            (x, y, width, height) = (data["left"][i], data["top"][i], data["width"][i], data["height"][i])
            coordinates.append([x, y, width, height])
            img = cv2.rectangle(img, (x, y), (x+width, y+height), (0,0,255), 2)
            print("\n" + data["text"][i] + "\nr_bot:(" + str(x+width) + "; " + str(y+height) + ")\nConfidence: " + str(data["conf"][i]))

    cv2.imshow("img", img)
    cv2.waitKey(0)

os.remove(imgFilename)