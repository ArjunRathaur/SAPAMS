from .dbutils import saveTeacher
from .teacher import Teacher

username = "teacher0"
password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8" # is "password"
firstname = "first0"
lastname = "last0"
email = "teacher0@sapams.com"
prefix = "Mr."

saveTeacher(Teacher(username, password, firstname, lastname, email, prefix))
