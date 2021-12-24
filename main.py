import cv2
import os   
import numpy as np
import pytesseract

# pytesseract.pytesseract.tesseract_cmd='C:\\Tess\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

path = "E:\python\mini project\images/"
files = [file for file in os.listdir(path) if file.endswith('.jpg') or file.endswith(".jfif") or file.endswith(".jpeg") or file.endswith(".png")]

for meter in files: 
    img = cv2.imread(path + meter)
    cv2.imshow('Original',img)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    (thresh, img) = cv2.threshold(img, 130, 220, cv2.THRESH_BINARY)
    cv2.imshow('Black white image', img)

    img = cv2.resize(img,(445, 127), interpolation=cv2.INTER_CUBIC)
    sharpening_filter = np.array([[-1,-1,-1],
                                  [-1,9,-1],
                                  [-1,-1,-1]])
    img = cv2.filter2D(img,-1,sharpening_filter)

    kernel = np.ones((2,2),np.uint8)
    kernel2 = np.ones((3,1),np.uint8)
    img = cv2.erode(img,kernel,iterations = 1)
    img = cv2.dilate(img,kernel2,iterations = 1)

    val= pytesseract.image_to_string(img)
    val = val.strip()
    val.replace(" ","")
    val.replace("\n","")
    val.replace("\t","")
    units=""
    count=0
    for i in val:
        for j in i:
            if j=='G' or j=='b':
                j='6'
            if j=='B':
                j='8'
            if j=='D':
                j='0'
            if j=='o' or j=='O':
                j='0'
            if j=='l' or j=='L' or j == 'I'or j=='t' or j == '|' or j=='!':
                j='1'
            if j=="Z" or j=='z' or j=='T':
                j='7'
        
        i = ''.join(char for char in i if i.isalnum())

        if i.isnumeric() or i=='.':
                units += i
                units.strip()
                units = units[len(units)-13:]
    units = units[:-1] + '.' + units[-1:]
    if units == '' or units == '.':
        tot = 0
    else: 
        tot= float(units)
    if(0<=tot<=30):
        payAmount=tot*4.00
        fixedcharge=100.00
    elif(31<=tot<100):
        payAmount=(30 * 4.00)+((tot-30)*5.45)
        fixedcharge=225.00
    elif(100<=tot<200):
        payAmount=(30 * 4.00)+(70*5.45)+((tot-100)*7.00)
        fixedcharge=250.00
    elif(200<tot):
        payAmount=(30 * 4.00)+(70*5.45)+(100*7.00)+((tot-200)*8.05)
        fixedcharge=300.00
    Total=payAmount+fixedcharge + (0.08 * tot) + (9/100 * payAmount)

    cv2.imshow('Result',img)
    cv2.waitKey(0)
cv2.destroyAllWindows() 