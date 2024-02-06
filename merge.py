import sys
import os
from pypdf import PdfWriter


def get_file_paths():
    answer = input("Enter the full path of the files you want to merge separated by a comma ','\n and in the order you want them to be merged: ")
    paths = answer.split(',')
    return(paths)

def get_title():
    return(input("Enter the title of the piece: "))

def check_files_exist(files):
    for path in files:
        if not os.path.isfile(path):
            print(path + " -- is not a supported file")
            return(False)
    return(True)
        

def merge_files(files, title):
    merger = PdfWriter()

    for pdf in files:
        merger.append(pdf)

    merger.write(title + ".pdf")
    merger.close()

if __name__ == "__main__":
    file_paths = get_file_paths()
    if check_files_exist(file_paths):
        merge_files(file_paths)