import cv2
import numpy as np
import pytesseract
import sqlite3

# pytesseract.pytesseract.tesseract_cmd='C:\\Tess\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

def ocr(Usid):
    conn = sqlite3.connect('userdata1.db')
    c=conn.cursor()

    c.execute(""" CREATE TABLE IF NOT EXISTS user1(
                    usid text,
                    prev_reading integer,
                    cur_reading integer,
                    mon_reading integer,
                    bill_amt integer,
                    img_path text)""")

    c.execute("SELECT img_path FROM user1 WHERE usid='{}'".format(Usid))
    img_data = c.fetchall()
    path= img_data[0][0]

    if path is not None:
        img = cv2.imread(path)
        cv2.imshow('Image captured', img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        (thresh, img) = cv2.threshold(img, 130, 220, cv2.THRESH_BINARY)

        img = cv2.resize(img, (445, 127), interpolation=cv2.INTER_CUBIC)
        sharpening_filter = np.array([[-1, -1, -1],
                                    [-1, 9, -1],
                                    [-1, -1, -1]])
        img = cv2.filter2D(img, -1, sharpening_filter)

        kernel = np.ones((2, 2), np.uint8)
        kernel2 = np.ones((3,1),np.uint8)
        img = cv2.erode(img, kernel, iterations=1)
        img = cv2.dilate(img, kernel2, iterations=1)

        val = pytesseract.image_to_string(img)
        val = val.strip()
        val.replace(" ", "")
        val.replace("\n", "")
        val.replace("\t", "")
        units = ""
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

            if i.isnumeric() or i == '.':
                units += i
                units.strip()
                units = units[len(units) - 13:]
        units = units[:-1] + '.' + units[-1:]
        if units == '' or units == '.':
            tot1 = 0
        else:
            tot1 = float(units)

        c.execute("SELECT prev_reading FROM user1 WHERE usid='{}'".format(Usid))
        data = c.fetchall()
        Prev_reading = float(data[0][0])
        Mon_reading = tot1 - Prev_reading
        tot= round(Mon_reading,2)
        if (0 <= tot <= 30):
            payAmount = tot * 4.00
            fixedcharge = 100.00
        elif (31 <= tot < 100):
            payAmount = (30 * 4.00) + ((tot - 30) * 5.45)
            fixedcharge = 225.00
        elif (100 <= tot < 200):
            payAmount = (30 * 4.00) + (70 * 5.45) + ((tot - 100) * 7.00)
            fixedcharge = 250.00
        elif (200 < tot):
            payAmount = (30 * 4.00) + (70 * 5.45) + (100 * 7.00) + ((tot - 200) * 8.05)
            fixedcharge = 300.00
        Total = round((payAmount + fixedcharge + (0.08 * tot) + (9 / 100 * payAmount)),2)



        c.execute("UPDATE user1 SET prev_reading='{}' , bill_amt='{}', cur_reading='{}',mon_reading='{}' WHERE usid='{}';".format(Prev_reading, Total, tot1,Mon_reading,Usid))

        # new_path='C:/Users/Admin/PycharmProjects/Mini_project//meter2.jpg' #path of the 9883.2 image for next month
        if(int(path[35])!=7):
            new_path='E:\python\mini project\images\meter'+str(int(path[35])+1)+'.jpg'
            c.execute("UPDATE user1 SET prev_reading='{}' , bill_amt='{}', cur_reading='{}',img_path='{}' WHERE usid='{}';".format(tot1, Total, 0.0, new_path , Usid))
        else:
            new_path='E:\python\mini project\images\meter1.jpg'
            c.execute("UPDATE user1 SET prev_reading='{}' , bill_amt='{}', cur_reading='{}',img_path='{}' WHERE usid='{}';".format(0, 0, 0.0, new_path , Usid))

        conn.commit()
        conn.close()
        cv2.waitKey()
        cv2.destroyAllWindows()
        return [Prev_reading,units,tot,Total]


