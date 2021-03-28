import mysql.connector as c


class Student:
    def __init__(self, UNIQUE_ID, NAME, BATCH_NAME):
        self.UNIQUE_ID = UNIQUE_ID
        self.NAME = NAME
        self.BATCH_NAME = BATCH_NAME
        self.STUDENT_DETAILS = (UNIQUE_ID, NAME, BATCH_NAME)
        pass


db = c.connect(
    host="localhost",
    user="root",
    password="2580",
    database='attendance'
)
cu = db.cursor()


def getAllStudents():
    sql = 'select * from student'
    cu.execute(sql)
    myResult = cu.fetchall()
    dictionary = dict()
    for i in myResult:
        dictionary[i[0]] = (i[1], i[2])

    return dictionary


ALL_STUDENTS = dict()

try:
    ALL_STUDENTS = dict(getAllStudents())
    print(ALL_STUDENTS)
except:
    pass


def addStudent():
    print('Welcome To Digital World')
    name = input("Enter Student's name\n")
    BATCH = input('Enter the BATCH\n')
    sql=f'insert into student (name,batch) values ("{name}","{BATCH}");'
    cu.execute(sql)
    db.commit()
    newSql=f'select unique_id from student where name="{name}" and batch="{BATCH}";'
    cu.execute(newSql)
    unique_id=cu.fetchall()
    print(f'Unique id of the student is {unique_id}')

    choice = input('Enter q to exit \n')
    if choice=='q' or choice=='Q':
        pass
    else:
        addStudent()

addStudent()

