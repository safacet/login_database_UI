import sys
from PyQt5 import QtWidgets
import sqlite3



class LoginScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.user_name = QtWidgets.QLineEdit()
        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login = QtWidgets.QPushButton("Login")
        self.text = QtWidgets.QLabel("")
        self.login_text = QtWidgets.QLabel("Username:")
        self.password_text = QtWidgets.QLabel("Password:")
        self.register = QtWidgets.QPushButton("Sign Up")

        h1_box = QtWidgets.QHBoxLayout()
        h1_box.addWidget(self.login_text)
        h1_box.addStretch()
        h1_box.addWidget(self.user_name)
        h2_box = QtWidgets.QHBoxLayout()
        h2_box.addWidget(self.password_text)
        h2_box.addStretch()
        h2_box.addWidget(self.password)
        h3_box = QtWidgets.QHBoxLayout()
        h3_box.addStretch()
        h3_box.addWidget(self.text)
        h3_box.addStretch()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h1_box)
        v_box.addLayout(h2_box)
        v_box.addLayout(h3_box)
        v_box.addStretch()
        v_box.addWidget(self.login)
        v_box.addWidget(self.register)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()

        self.setLayout(h_box)
        self.setWindowTitle("User Login")
        self.login.clicked.connect(self.log_in)
        self.register.clicked.connect(self.signup)

        self.show()

    def log_in(self):
        name = self.user_name.text()
        passw = self.password.text()
        query = "select * from users where Username = ? and Password = ?"
        database.cursor.execute(query, (name, passw))
        infos = database.cursor.fetchall()
        if len(infos) == 0:
            self.text.setText("Access Denied!")
            self.user_name.selectAll()
            self.password.selectAll()

        else:
            self.text.setText("Access Granted!")
            self.second = Secondscreen(name)
            self.close()


    def signup(self):
        name = self.user_name.text()
        passw = self.password.text()

        query = "Insert into users (Username, Password) values(?, ?)"
        database.cursor.execute(query, (name, passw))
        database.con.commit()
        self.text.setText("Sign up successful\nYou can log in")


class Secondscreen(QtWidgets.QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("User Interface")
        self.top = QtWidgets.QLabel("Personal Informations:")
        self.name_text = QtWidgets.QLabel("Name:")
        self.name = QtWidgets.QLineEdit()
        self.surname_text = QtWidgets.QLabel("Surname:")
        self.surname = QtWidgets.QLineEdit()
        self.height_text = QtWidgets.QLabel("Your Height:")
        self.height_ = QtWidgets.QLineEdit()
        self.inform = QtWidgets.QLabel("Update or collect \nyour informations ")

        self.collect_but = QtWidgets.QPushButton("Collect Info")
        self.updatebutton = QtWidgets.QPushButton("Update Info")

        h1_box = QtWidgets.QHBoxLayout()
        h1_box.addStretch()
        h1_box.addWidget(self.top)
        h1_box.addStretch()
        h2_box = QtWidgets.QHBoxLayout()
        h2_box.addWidget(self.name_text)
        h2_box.addStretch()
        h2_box.addWidget(self.name)
        h3_box = QtWidgets.QHBoxLayout()
        h3_box.addWidget(self.surname_text)
        h3_box.addStretch()
        h3_box.addWidget(self.surname)
        h4_box = QtWidgets.QHBoxLayout()
        h4_box.addWidget(self.height_text)
        h4_box.addStretch()
        h4_box.addWidget(self.height_)
        h5_box = QtWidgets.QHBoxLayout()
        h5_box.addStretch()
        h5_box.addWidget(self.inform)
        h5_box.addStretch()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h1_box)
        v_box.addLayout(h2_box)
        v_box.addLayout(h3_box)
        v_box.addLayout(h4_box)
        v_box.addStretch()
        v_box.addLayout(h5_box)
        v_box.addWidget(self.collect_but)
        v_box.addWidget(self.updatebutton)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()

        self.setLayout(h_box)

        self.collect_but.clicked.connect(self.get_info)
        self.updatebutton.clicked.connect(self.update_info)

        self.show()

    def get_info(self):
        query = "select Name, Surname, Height from users where Username = ?"
        database.cursor.execute(query,(self.user,))
        infos = database.cursor.fetchall()
        self.name.setText(infos[0][0])
        self.surname.setText(infos[0][1])
        self.height_.setText(str(infos[0][2]))
        self.inform.setText("Your Infos Collected\nYou can update them")

    def update_info(self):
        name = self.name.text()
        surname = self.surname.text()
        height = int(self.height_.text())
        query = "update users set Name = ?, Surname = ?, Height = ? where Username = ?"
        database.cursor.execute(query, (name, surname, height, self.user))
        database.con.commit()
        self.inform.setText("Infos have been updated!")


class Database():
    def __init__(self):
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.connect()


    def connect(self):
        query = "create table if not exists users(Username TEXT, Password TEXT, Name TEXT, Surname TEXT, Height INT)"
        self.cursor.execute(query)
        self.con.commit()



app = QtWidgets.QApplication(sys.argv)

database = Database()
loginscreen = LoginScreen()

sys.exit(app.exec_())