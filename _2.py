# Клас Викладач
class Teacher:
    university_name = "КНУ"   # статичний атрибут

    def __init__(self, name):
        self.name = name
        self.students = []      # один-до-багатьох
        self.classrooms = []    # багато-до-багатьох

    # додати студента
    def add_student(self, student):
        self.students.append(student)
        student.teacher = self

    # додати аудиторію
    def add_classroom(self, room):
        self.classrooms.append(room)
        room.teachers.append(self)

    @staticmethod
    def show_university():
        print("Університет:", Teacher.university_name)


# Клас Студент
class Student:
    students_count = 0   # статичний атрибут

    def __init__(self, name):
        self.name = name
        self.teacher = None      # один-до-одного
        self.classrooms = []     # багато-до-багатьох
        Student.students_count += 1

    # запис у аудиторію
    def join_classroom(self, room):
        self.classrooms.append(room)
        room.students.append(self)

    @staticmethod
    def show_students_count():
        print("Кількість студентів:", Student.students_count)


# Клас Аудиторія
class Classroom:
    rooms_count = 0   # статичний атрибут

    def __init__(self, number):
        self.number = number
        self.students = []   # багато-до-багатьох
        self.teachers = []   # багато-до-багатьох
        Classroom.rooms_count += 1

    def show_students(self):
        print(f"\nСтуденти в аудиторії {self.number}:")
        for student in self.students:
            print(student.name)

    @staticmethod
    def show_rooms_count():
        print("Кількість аудиторій:", Classroom.rooms_count)


# -------------------
# Створення об'єктів

teacher = Teacher("Іваненко")

student1 = Student("Олег")
student2 = Student("Марія")

room1 = Classroom(101)
room2 = Classroom(202)

# один-до-багатьох
teacher.add_student(student1)
teacher.add_student(student2)

# багато-до-багатьох
teacher.add_classroom(room1)
teacher.add_classroom(room2)

student1.join_classroom(room1)
student1.join_classroom(room2)

student2.join_classroom(room1)

# -------------------
# Перевірка

Teacher.show_university()

Student.show_students_count()

Classroom.show_rooms_count()

room1.show_students()