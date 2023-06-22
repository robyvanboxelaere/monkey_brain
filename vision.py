# Imports
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def read_cash():
    # Read money.png
    img = Image.open('money.png')

    # Convert to grayscale
    img = img.convert('L')

    # Make all pixels <= rgb(220, 220, 220) black
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pixels[i, j] <= 254:
                pixels[i, j] = 0

    # Save grayscale image
    img.save('money_converted.png')

    # Convert to text
    cashAmount = pytesseract.image_to_string(img)

    # Remove every non integer
    cashAmount = ''.join(filter(str.isdigit, cashAmount))

    return cashAmount

print(read_cash())