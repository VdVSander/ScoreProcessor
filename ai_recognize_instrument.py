from music21 import *

# Load the PDF file as a stream object
score = converter.parse('The Mask of Zorro.pdf')

# Extract the parts from the stream object
parts = instrument.partitionByInstrument(score)

# Loop over the parts and print the instrument name
for part in parts:
    # If the part has a defined instrument name, print it
    if part.partName is not None:
        print(part.partName)
