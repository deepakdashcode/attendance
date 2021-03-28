import mysql.connector as c
import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

db = c.connect(
    host="localhost",
    user="root",
    password="2580",
    database='attendance'
)

cu = db.cursor()


def getCurrentAttendances():
    sql = 'select * from attendance'
    cu.execute(sql)
    myResult = cu.fetchall()
    return myResult


getCurrentAttendances()


def getAllStudents():
    sql = 'select * from student'
    cu.execute(sql)
    myResult = cu.fetchall()
    dictionary = dict()
    for i in myResult:
        dictionary[i[0]] = (i[1], i[2])

    return dictionary


ALL_STUDENTS = getAllStudents()


def takeUniqueID():
    while True:
        from datetime import date
        from datetime import datetime

        currentDate = date.today()  # YYYY-MM-DT

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        ###########################################

        success, img = cap.read()
        for barcode in decode(img):
            myData = barcode.data.decode('utf-8')
            # MAKING BOUNDARY
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            pts2 = barcode.rect
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            print(myData)

        cv2.imshow('Result', img)
        cv2.waitKey(1)

        ##########################################

        try:
            unique_id =myData
        except:
            pass

        #unique_id = input('Enter the unique id\n')

        # Checking if unique id is valid
        sql = 'select unique_id from student'
        cu.execute(sql)
        myRes = cu.fetchall()  # To get unique ids in [(10000001,), (10000002,), (10000003,), (10000004,)] format
        allIds = []
        for i in myRes:
            allIds.append(i[0])

        is_valid_id = False

        try:
            if int(unique_id) in allIds:
                is_valid_id = True
        except:
            pass

        if is_valid_id:
            toAdd = True
            unique_id = int(unique_id)
            NAME = ALL_STUDENTS[unique_id][0]
            BATCH = ALL_STUDENTS[unique_id][1]
            currentTuple=(NAME,unique_id,BATCH)
            # print('Current Tuple is ',currentTuple)
            currentAttendances=getCurrentAttendances()
            # print(currentAttendances)
            for i in currentAttendances:
                #print(i[1])
                if NAME == i[0] and currentDate == i[3]:
                    toAdd=False



            if toAdd:
                unique_id = int(unique_id)
                NAME = ALL_STUDENTS[unique_id][0]
                BATCH = ALL_STUDENTS[unique_id][1]
                sql = f'insert into attendance values ("{NAME}",{unique_id},"{BATCH}","{currentDate}","{current_time}")'
                cu.execute(sql)
                db.commit()
                print(f'WELCOME {NAME}')
                pass
            else:
                pass


        else:
            pass
            #print('INVALID ID')

takeUniqueID()
