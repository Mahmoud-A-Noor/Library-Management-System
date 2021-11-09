import datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import MySQLdb
import sys
from xlsxwriter import *
from xlrd import *
import pyqtgraph as pg

MainUi,_ = loadUiType('GUI.ui')

employee_id = 0
employee_branch = 0

class Main(QMainWindow,MainUi):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.UI_Changes()
        self.DB_Connect()
        self.Handle_Buttons()
        self.Open_Login_Tab()
        self.Show_All_Categories()
        self.Show_Publisher()
        self.Show_Branches()
        self.Show_Author()
        self.Show_All_Books()
        self.Show_All_Clients()
        self.Show_History()
        self.Retrieve_ToDay_Work()
        self.Show_Employees()
        self.dateEdit_6.setDate(QDate(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day))
        self.dateEdit_7.setDate(QDate(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day))
        self.get_dashboard_data()

    def UI_Changes(self):
        self.tabWidget.tabBar().setVisible(False)


    def DB_Connect(self):
        self.db = MySQLdb.connect(user="root",password="root",host="localhost",db="library")
        self.cur = self.db.cursor()


    def Handle_Buttons(self):
        self.pushButton.clicked.connect(self.Open_Daily_Movements_Tab)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_3.clicked.connect(self.Open_Clients_Tab)
        self.pushButton_6.clicked.connect(self.Open_Dashboard_Tab)
        self.pushButton_4.clicked.connect(self.Open_History_Tab)
        self.pushButton_5.clicked.connect(self.Open_Report_Tab)
        self.pushButton_7.clicked.connect(self.Open_Settings_Tab)
        self.pushButton_8.clicked.connect(self.Handle_ToDay_Work)

        self.pushButton_19.clicked.connect(self.Add_Branch)
        self.pushButton_20.clicked.connect(self.Add_Publisher)
        self.pushButton_21.clicked.connect(self.Add_Author)
        self.pushButton_22.clicked.connect(self.Add_Category)
        self.pushButton_27.clicked.connect(self.Add_Employee)
        self.pushButton_10.clicked.connect(self.Add_New_Book)
        self.pushButton_15.clicked.connect(self.Add_New_Client)

        self.pushButton_12.clicked.connect(self.Edit_Book_Search)
        self.pushButton_11.clicked.connect(self.Edit_Book)
        self.pushButton_13.clicked.connect(self.Delete_Book)
        self.pushButton_9.clicked.connect(self.All_Books_Filter)

        self.pushButton_17.clicked.connect(self.Edit_Client_Search)
        self.pushButton_16.clicked.connect(self.Edit_Client)
        self.pushButton_18.clicked.connect(self.Delete_Client)

        self.pushButton_30.clicked.connect(self.Check_Employee)
        self.pushButton_29.clicked.connect(self.Edit_Employee_Data)

        self.pushButton_41.clicked.connect(self.Open_Login_Tab)
        self.pushButton_39.clicked.connect(self.Open_Reset_Password_Tab)

        self.pushButton_28.clicked.connect(self.Add_Employee_Permission)
        self.pushButton_35.clicked.connect(self.Book_Export_Report)
        self.pushButton_37.clicked.connect(self.Clients_Export_Report)
        self.pushButton_38.clicked.connect(self.Handle_Login)
        self.pushButton_43.clicked.connect(self.get_dashboard_data)

    def Handle_Login(self):
        username = self.lineEdit_40.text()
        password = self.lineEdit_41.text()

        sql = """SELECT * FROM employee WHERE name = %s and password = %s"""
        row_count = self.cur.execute(sql, ([username, password]))
        if row_count == 0:
            QMessageBox.information(self, "Error", "Please, Check Your Name and Password then Try Again")
        else:
            data = self.cur.fetchone()
            global employee_id,employee_branch
            employee_id = data[0]
            employee_branch = data[6]

            self.groupBox_14.setEnabled(True)
            sql = """SELECT * FROM employee_permissions WHERE employee_name = %s"""
            self.cur.execute(sql, ([username]))
            data = self.cur.fetchone()

            self.pushButton.setEnabled(True)
            if data[2]:
                self.pushButton_2.setEnabled(True)
            if data[3]:
                self.pushButton_3.setEnabled(True)
            if data[4]:
                self.pushButton_6.setEnabled(True)
            if data[5]:
                self.pushButton_4.setEnabled(True)
            if data[6]:
                self.pushButton_5.setEnabled(True)
            if data[7]:
                self.pushButton_7.setEnabled(True)
            if data[8]:
                self.pushButton_10.setEnabled(True)
            if data[9]:
                self.pushButton_11.setEnabled(True)
            if data[10]:
                self.pushButton_13.setEnabled(True)
            if data[11]:
                self.pushButton_34.setEnabled(True)
            if data[12]:
                self.pushButton_35.setEnabled(True)
            if data[13]:
                self.pushButton_15.setEnabled(True)
            if data[14]:
                self.pushButton_16.setEnabled(True)
            if data[15]:
                self.pushButton_18.setEnabled(True)
            if data[16]:
                self.pushButton_36.setEnabled(True)
            if data[17]:
                self.pushButton_37.setEnabled(True)
            if data[18]:
                self.pushButton_19.setEnabled(True)
            if data[19]:
                self.pushButton_20.setEnabled(True)
            if data[20]:
                self.pushButton_21.setEnabled(True)
            if data[21]:
                self.pushButton_22.setEnabled(True)
            if data[22]:
                self.pushButton_27.setEnabled(True)
            if data[23]:
                self.pushButton_29.setEnabled(True)

            date = datetime.datetime.now()
            self.cur.execute('''
                    INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                    VALUES (%s,%s,%s,%s,%s)
                    ''', (employee_id, 1, 7, date, employee_branch))

            self.Show_History()
            self.Open_Daily_Movements_Tab()



    def Handle_Reset_Password(self):
        pass

    def Handle_ToDay_Work(self):
        book_title = self.lineEdit.text()
        type = self.comboBox.currentIndex()
        client_national_id = self.lineEdit_8.text()
        from_date = str(datetime.date.today())
        to_date = self.dateEdit_6.date().toString("yyyy-MM-dd")
        date = datetime.datetime.now()
        branch = 1
        employee = 3


        self.cur.execute('''
        INSERT INTO dailymovements(book_id, client_id, type, date, branch_id, book_from, book_to, employee_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ''',(book_title,client_national_id,type,date,branch,from_date,to_date,employee))

        date = datetime.datetime.now()
        global employee_id, employee_branch
        self.cur.execute('''
                INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                VALUES (%s,%s,%s,%s,%s)
                ''', (employee_id, 3, 8, date, employee_branch))
        self.db.commit()

        self.Show_History()
        self.Retrieve_ToDay_Work()


    def Retrieve_ToDay_Work(self):
        self.cur.execute('''
        SELECT book_id, type, client_id, book_from, book_to FROM dailymovements
        ''')

        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        for row,form in enumerate(data):
            for col,item in enumerate(form):
                if col == 1:
                    if item == 0:
                        self.tableWidget.setItem(row,col,QTableWidgetItem("Rent"))
                    else:
                        self.tableWidget.setItem(row, col, QTableWidgetItem("Retrieve"))
                elif col == 2:
                    sql = ('''
                    SELECT name FROM clients WHERE national_id = %s
                    ''')
                    self.cur.execute(sql,[(item)])
                    client_name = self.cur.fetchone()
                    if client_name != None:
                        self.tableWidget.setItem(row, col, QTableWidgetItem(client_name[0]))
                    else:
                        self.tableWidget.setItem(row, col, QTableWidgetItem(f"{item} Not A Client"))
                else:
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(item)))
            row_pos = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_pos)

######################################################

    def Show_All_Books(self):
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)

        self.cur.execute('''
        SELECT code,title,category_id,author_id,price
        FROM books
        ''')
        books = self.cur.fetchall()

        for row,data in enumerate(books):
            for col,item in enumerate(data):
                if col == 2:
                    sql = ('''SELECT category_name FROM category WHERE id = %s''')
                    self.cur.execute(sql,[(item)])
                    category_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(category_name[0])))

                elif col == 3:
                    sql = ('''SELECT name FROM author WHERE id = %s''')
                    self.cur.execute(sql, [(item+1)])
                    author_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(author_name[0])))

                else:
                    self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(item)))
            row_pos = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_pos)

    def All_Books_Filter(self):
        title = self.lineEdit_2.text()
        category = self.comboBox_2.currentIndex()

        if category == 0:
            sql = ('''
                    SELECT code, title, category_id, author_id, publisher_id FROM books WHERE title = %s and category_id = %s
                    ''')
        else:
            sql = ('''SELECT code, title, category_id, author_id, publisher_id FROM books WHERE title = %s''')
        self.cur.execute(sql, ([title, category]))
        books = self.cur.fetchall()

        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)

        for row, data in enumerate(books):
            for col, item in enumerate(data):
                if col == 2:
                    sql = ('''SELECT category_name FROM category WHERE id = %s''')
                    self.cur.execute(sql, [(item)])
                    category_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(category_name[0])))

                elif col == 3:
                    sql = ('''SELECT name FROM author WHERE id = %s''')
                    self.cur.execute(sql, [(item + 1)])
                    author_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(author_name[0])))

                else:
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
            row_pos = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_pos)


    def Add_New_Book(self):
        book_title = self.lineEdit_3.text()
        category = self.comboBox_3.currentIndex()
        description = self.textEdit.toPlainText()
        price = self.lineEdit_4.text()
        code = self.lineEdit_5.text()
        publisher = self.comboBox_4.currentIndex()
        author = self.comboBox_5.currentIndex()
        state = self.comboBox_6.currentIndex()
        part_order = self.lineEdit_39.text()
        barcode = self.lineEdit_50.text()

        date = datetime.datetime.now()

        self.cur.execute('''
        INSERT INTO books(title, description, category_id, code, barcode, part_order, price, publisher_id, author_id, status, date)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''',(book_title,description,category,code,barcode,part_order,price,publisher,author,state,date))

        global employee_id, employee_branch
        self.cur.execute('''
                INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                VALUES (%s,%s,%s,%s,%s)
                ''', (employee_id, 3, 1, date, employee_branch))
        self.db.commit()

        self.Show_History()
        self.Show_All_Books()

    def Edit_Book_Search(self):
        book_code = self.lineEdit_9.text()
        sql = ('''
        SELECT * FROM books WHERE code = %s
        ''')
        self.cur.execute(sql,[(book_code)])
        data = self.cur.fetchone()

        self.lineEdit_7.setText(str(data[1]))
        self.textEdit_2.setText(str(data[2]))
        self.comboBox_10.setCurrentIndex(int(data[-1]))
        self.lineEdit_6.setText(str(data[6]))
        self.comboBox_7.setCurrentIndex(int(data[-3]))
        self.comboBox_8.setCurrentIndex(int(data[-2]))
        self.comboBox_9.setCurrentIndex(int(data[-5]))
        self.lineEdit_51.setText(str(data[5]))

        date = datetime.datetime.now()
        global employee_id, employee_branch
        self.cur.execute('''
                INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                VALUES (%s,%s,%s,%s,%s)
                ''', (employee_id, 6, 1, date, employee_branch))

        self.Show_History()

    def Edit_Book(self):
        book_title = self.lineEdit_7.text()
        category = self.comboBox_10.currentIndex()
        description = self.textEdit_2.toPlainText()
        price = self.lineEdit_6.text()
        code = self.lineEdit_9.text()
        publisher = self.comboBox_7.currentIndex()
        author = self.comboBox_8.currentIndex()
        state = self.comboBox_9.currentIndex()
        part_order = self.lineEdit_51.text()

        self.cur.execute('''
                UPDATE books SET title = %s, description = %s, category_id = %s, code = %s, part_order = %s, price = %s, publisher_id = %s, author_id = %s, status = %s WHERE code = %s
                ''', (book_title, description, category, code, part_order, price, publisher, author, state, code))

        date = datetime.datetime.now()
        global employee_id, employee_branch
        self.cur.execute('''
                        INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                        VALUES (%s,%s,%s,%s,%s)
                        ''', (employee_id, 4, 1, date, employee_branch))
        self.db.commit()
        QMessageBox.information(self,"success","information updated successfully")

        self.Show_History()
        self.Show_All_Books()


    def Delete_Book(self):
        code = self.lineEdit_9.text()

        TOF = QMessageBox.warning(self,"Delete Book","Are You sure You Want To Delete The Book ?",QMessageBox.Yes | QMessageBox.No)
        if TOF == QMessageBox.Yes:
            sql = ('''DELETE FROM books WHERE code = %s''')
            self.cur.execute(sql, [(code)])

            date = datetime.datetime.now()
            global employee_id, employee_branch
            self.cur.execute('''
                                    INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                                    VALUES (%s,%s,%s,%s,%s)
                                    ''', (employee_id, 5, 1, date, employee_branch))
            self.db.commit()
            QMessageBox.information(self, "success", "The Book Deleted successfully")

            self.Show_History()
            self.Show_All_Books()
######################################################


######################################################

    def Show_All_Clients(self):
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.insertRow(0)

        self.cur.execute('''
                SELECT name,mail,phone,national_id,date
                FROM clients
                ''')
        clients = self.cur.fetchall()

        for row, data in enumerate(clients):
            for col, item in enumerate(data):
                self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(item)))
            row_pos = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_pos)



    def Add_New_Client(self):
        name = self.lineEdit_11.text()
        mail = self.lineEdit_12.text()
        phone = self.lineEdit_13.text()
        national_id = self.lineEdit_14.text()

        date = datetime.datetime.now()

        self.cur.execute('''
                INSERT INTO clients(name,mail,phone,national_id,date)
                VALUES (%s,%s,%s,%s,%s)
                ''', (name, mail, phone, national_id, date))

        global employee_id, employee_branch
        self.cur.execute('''
                INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                VALUES (%s,%s,%s,%s,%s)
                ''', (employee_id, 3, 1, date, employee_branch))

        self.db.commit()
        QMessageBox.information(self, "success", "Client Added Successfully")

        self.Show_History()
        self.Show_All_Clients()

    def Edit_Client_Search(self):
        client_data = self.lineEdit_19.text()

        if self.comboBox_11.currentIndex() == 0:
            sql = ('''SELECT * FROM clients WHERE name = %s''')
            self.cur.execute(sql, [(client_data)])
            data = self.cur.fetchone()

        elif self.comboBox_11.currentIndex() == 1:
            sql = ('''SELECT * FROM clients WHERE mail = %s''')
            self.cur.execute(sql, [(client_data)])
            data = self.cur.fetchone()

        elif self.comboBox_11.currentIndex() == 2:
            sql = ('''SELECT * FROM clients WHERE phone = %s''')
            self.cur.execute(sql, [(client_data)])
            data = self.cur.fetchone()

        elif self.comboBox_11.currentIndex() == 3:
            sql = ('''SELECT * FROM clients WHERE national_id = %s''')
            self.cur.execute(sql, [(client_data)])
            data = self.cur.fetchone()

        self.lineEdit_15.setText(data[1])
        self.lineEdit_16.setText(data[2])
        self.lineEdit_17.setText(data[3])
        self.lineEdit_18.setText(data[5])

        date = datetime.datetime.now()
        global employee_id, employee_branch
        self.cur.execute('''
                INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                VALUES (%s,%s,%s,%s,%s)
                ''', (employee_id, 6, 2, date, employee_branch))

        self.Show_History()

    def Edit_Client(self):

        name = self.lineEdit_15.text()
        mail = self.lineEdit_16.text()
        phone = self.lineEdit_17.text()
        national_id = self.lineEdit_18.text()

        self.cur.execute('''
        UPDATE clients SET name = %s, mail = %s, phone = %s, national_id = %s WHERE national_id = %s
        ''',(name,mail,phone,national_id,national_id))

        date = datetime.datetime.now()
        global employee_id, employee_branch
        self.cur.execute('''
                        INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                        VALUES (%s,%s,%s,%s,%s)
                        ''', (employee_id, 4, 2, date, employee_branch))

        self.db.commit()
        QMessageBox.information(self, "success", "information updated successfully")

        self.Show_History()
        self.Show_All_Clients()

    def Delete_Client(self):
        client_data = self.lineEdit_19.text()

        TOF = QMessageBox.warning(self, "Delete Book", "Are You sure You Want To Delete The Book ?",QMessageBox.Yes | QMessageBox.No)
        if TOF == QMessageBox.Yes:
            if self.comboBox_11.currentIndex() == 0:
                sql = ('''DELETE FROM clients WHERE name = %s''')
                self.cur.execute(sql, [(client_data)])

            elif self.comboBox_11.currentIndex() == 1:
                sql = ('''DELETE FROM clients WHERE mail = %s''')
                self.cur.execute(sql, [(client_data)])

            elif self.comboBox_11.currentIndex() == 2:
                sql = ('''DELETE FROM clients WHERE phone = %s''')
                self.cur.execute(sql, [(client_data)])

            elif self.comboBox_11.currentIndex() == 3:
                sql = ('''DELETE FROM clients WHERE national_id = %s''')
                self.cur.execute(sql, [(client_data)])

            date = datetime.datetime.now()
            global employee_id, employee_branch
            self.cur.execute('''
                                    INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                                    VALUES (%s,%s,%s,%s,%s)
                                    ''', (employee_id, 5, 2, date, employee_branch))

            self.db.commit()
            QMessageBox.information(self, "success", "Client Deleted successfully")

            self.Show_History()
            self.Show_All_Clients()

######################################################
##### History
    def Show_History(self):

        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.insertRow(0)
        self.cur.execute('''
                SELECT employee_id, employee_action, affected_table, branch, operation_date
                FROM history
                ''')
        history = self.cur.fetchall()

        for row, data in enumerate(history):
            for col, item in enumerate(data):
                if col == 0:
                    sql = ('''SELECT name FROM employee WHERE id = %s''')
                    self.cur.execute(sql, [(item)])
                    employee_name = self.cur.fetchone()
                    self.tableWidget_4.setItem(row, col, QTableWidgetItem(employee_name[0]))

                elif col == 3:
                    sql = ('''SELECT name FROM branch WHERE id = %s''')
                    self.cur.execute(sql, [(item)])
                    branch_name = self.cur.fetchone()
                    self.tableWidget_4.setItem(row, col, QTableWidgetItem(branch_name[0]))

                elif col == 4:
                    self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(item)))

                else:
                    item = int(item)
                    if col == 1:
                        action =" "
                        if item == 1:
                            action = "Login"
                        if item == 2:
                            action = "Logout"
                        if item == 3:
                            action = "Add"
                        if item == 4:
                            action = "Edit"
                        if item == 5:
                            action = "Delete"
                        if item == 6:
                            action = "Search"
                        self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(action)))

                    if col == 2:
                        table =" "
                        if item == 1:
                            table = "Books"
                        if item == 2:
                            table = "Clients"
                        if item == 3:
                            table = "History"
                        if item == 4:
                            table = "Branch"
                        if item == 5:
                            table = "Category"
                        if item == 6:
                            table = "Daily Movements"
                        if item == 7:
                            table = "Employee"
                        if item == 8:
                            table = "Publisher"
                        self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(table)))

            row_pos = self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_pos)

######################################################
##### books report

    def All_Books_Report(self):
        pass
    def Books_Filter_Report(self):
        pass
    def Book_Export_Report(self):
        self.cur.execute("""
        SELECT * FROM books
        """)
        data = self.cur.fetchall()

        file = Workbook("books_report.xlsx")
        sheet1 = file.add_worksheet()
        sheet1.write(0,0,"ID")
        sheet1.write(0,1,"Book Title")
        sheet1.write(0,2,"Description")
        sheet1.write(0,3,"Book Code")
        sheet1.write(0,4,"Barcode")
        sheet1.write(0,5,"Part_order")
        sheet1.write(0,6,"Price")
        sheet1.write(0,7,"Image")
        sheet1.write(0,8,"status")
        sheet1.write(0,9,"date")
        sheet1.write(0,10,"Publisher_ID")
        sheet1.write(0,11,"Author_ID")
        sheet1.write(0,12,"Category_ID")

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number,column_number,str(item))
                column_number+=1
            row_number+=1

        file.close()
        QMessageBox.information(self, "success", "Books Exported Successfully")


######################################################
##### Client report

    def All_Clients_Report(self):
        pass
    def Clients_Filter_Report(self):
        pass
    def Clients_Export_Report(self):
        self.cur.execute("""
                SELECT * FROM clients
                """)
        data = self.cur.fetchall()

        file = Workbook("clients_report.xlsx")
        sheet1 = file.add_worksheet()
        sheet1.write(0, 0, "ID")
        sheet1.write(0, 1, "Name")
        sheet1.write(0, 2, "E-Mail")
        sheet1.write(0, 3, "Phone Number")
        sheet1.write(0, 4, "Date")
        sheet1.write(0, 5, "National ID")

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1

        file.close()
        QMessageBox.information(self, "success", "Clients Exported Successfully")

####################################################
#####
    def Monthly_Report(self):
        pass
    def Monthly_Export_Report(self):
        pass

###################################################
##### Settings

    def Add_Branch(self):
        branch_name = self.lineEdit_20.text()
        branch_code = self.lineEdit_21.text()
        branch_location = self.lineEdit_22.text()

        self.cur.execute('''
        INSERT INTO branch(name,code,location)
        VALUES (%s,%s,%s)
        ''',(branch_name,branch_code,branch_location))

        date = datetime.datetime.now()
        global employee_id, employee_branch
        self.cur.execute('''
                INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                VALUES (%s,%s,%s,%s,%s)
                ''', (employee_id, 3, 3, date, employee_branch))
        self.db.commit()

        self.Show_History()
        self.Show_Branches()

    def Add_Publisher(self):
        publisher_name = self.lineEdit_23.text()
        publisher_location = self.lineEdit_24.text()

        self.cur.execute('''
                INSERT INTO publisher(name,location)
                VALUES (%s,%s)
                ''', (publisher_name, publisher_location))

        date = datetime.datetime.now()
        global employee_id, employee_branch
        self.cur.execute('''
                INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                VALUES (%s,%s,%s,%s,%s)
                ''', (employee_id, 3, 5, date, employee_branch))
        self.db.commit()

        self.Show_History()
        self.Show_Publisher()

    def Add_Author(self):
        author_name = self.lineEdit_26.text()
        author_location = self.lineEdit_27.text()

        self.cur.execute('''
                        INSERT INTO author(name,location)
                        VALUES (%s,%s)
                        ''', (author_name, author_location))

        date = datetime.datetime.now()
        global employee_id, employee_branch
        self.cur.execute('''
                INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                VALUES (%s,%s,%s,%s,%s)
                ''', (employee_id, 3, 6, date, employee_branch))
        self.db.commit()

        self.Show_History()
        self.Show_Author()

    def Add_Category(self):
        category_name = self.lineEdit_28.text()
        parent_category = self.comboBox_13.currentText()
        self.cur.execute('''
        INSERT INTO category(category_name,parent_category)
        VALUES (%s,%s)
        ''',(category_name,parent_category))

        date = datetime.datetime.now()
        global employee_id, employee_branch
        self.cur.execute('''
                INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                VALUES (%s,%s,%s,%s,%s)
                ''', (employee_id, 3, 4, date, employee_branch))
        self.db.commit()

        self.Show_All_Categories()
        self.Show_History()

    def Show_All_Categories(self):
        self.cur.execute('''
        SELECT category_name FROM category
        ''')
        categories = self.cur.fetchall()
        self.comboBox_13.clear()
        for category in categories:
            self.comboBox_13.addItem(category[0])
            self.comboBox_3.addItem(category[0])
            self.comboBox_10.addItem(category[0])
            self.comboBox_2.addItem(category[0])

    def Show_Branches(self):

        self.cur.execute('''
        SELECT name FROM branch
        ''')
        branches = self.cur.fetchall()
        for branch in branches:
            self.comboBox_21.addItem(branch[0])
            self.comboBox_22.addItem(branch[0])

    def Show_Publisher(self):
        self.cur.execute('''
                SELECT name FROM publisher
                ''')
        publishers = self.cur.fetchall()
        for publisher in publishers:
            self.comboBox_4.addItem(publisher[0])
            self.comboBox_7.addItem(publisher[0])

    def Show_Author(self):
        self.cur.execute('''
                        SELECT name FROM author
                        ''')
        authors = self.cur.fetchall()
        for author in authors:
            self.comboBox_8.addItem(author[0])
            self.comboBox_5.addItem(author[0])

    def Show_Employees(self):
        self.cur.execute("""
        SELECT name FROM employee
        """)
        employees = self.cur.fetchall()
        for employee in employees:
            self.comboBox_19.addItem(employee[0])
            self.comboBox_23.addItem(employee[0])

###################################################
#####
    def Add_Employee(self):

        employee_name = self.lineEdit_33.text()
        employee_mail = self.lineEdit_31.text()
        employee_phone = self.lineEdit_34.text()
        employee_branch_ = self.comboBox_21.currentIndex()
        employee_national_id = self.lineEdit_32.text()
        employee_priority = self.lineEdit_37.text()
        employee_password = self.lineEdit_35.text()
        employee_password2 = self.lineEdit_36.text()

        date = datetime.datetime.now()

        if(employee_password == employee_password2):
            self.cur.execute('''
            INSERT INTO employee (name,mail,phone,branch,date,national_id,priority,password)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(employee_name, employee_mail, employee_phone, employee_branch_, date, employee_national_id, employee_priority, employee_password))

            date = datetime.datetime.now()
            global employee_id, employee_branch
            self.cur.execute('''
                INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                VALUES (%s,%s,%s,%s,%s)
                ''', (employee_id, 3, 7, date, employee_branch))
            self.db.commit()
            self.lineEdit_33.setText("")
            self.lineEdit_31.setText("")
            self.lineEdit_34.setText("")
            self.lineEdit_32.setText("")
            self.lineEdit_37.setText("")
            self.lineEdit_35.setText("")
            self.lineEdit_36.setText("")
            self.comboBox_21.setCurrentIndex(0)
            QMessageBox.information(self, "success", "Employee Added Successfully")

            self.Show_History()
        else:
            QMessageBox.information(self,"Error","Please, Check Your Password And Try Again")

    def Check_Employee(self):
        name = self.lineEdit_45.text()
        password = self.lineEdit_48.text()

        sql = """SELECT * FROM employee WHERE name = %s and password = %s"""
        row_count = self.cur.execute(sql,([name,password]))
        if row_count == 0:
            QMessageBox.information(self, "Error", "Please, Check Your Name and Password then Try Again")
        else:
            data = self.cur.fetchone()
            self.groupBox_9.setEnabled(True)
            self.lineEdit_43.setText(str(data[2]))
            self.lineEdit_46.setText(str(data[3]))
            self.lineEdit_44.setText(str(data[5]))
            self.comboBox_22.setCurrentIndex(data[-3])
            self.lineEdit_49.setText(str(data[-2]))
            self.lineEdit_47.setText(str(data[-1]))



    def Edit_Employee_Data(self):
        name = self.lineEdit_45.text()
        password = self.lineEdit_47.text()
        email = self.lineEdit_43.text()
        phone = self.lineEdit_46.text()
        national_id = self.lineEdit_44.text()
        branch = self.comboBox_22.currentIndex()
        priority = self.lineEdit_49.text()

        self.cur.execute("""
        UPDATE employee SET mail=%s, phone=%s, national_id=%s, branch=%s, priority=%s, password=%s WHERE name = %s
        """,(email,phone,national_id,branch,priority,password,name))

        date = datetime.datetime.now()
        global employee_id, employee_branch
        self.cur.execute('''
                INSERT INTO history(employee_id, employee_action, affected_table, operation_date, branch)
                VALUES (%s,%s,%s,%s,%s)
                ''', (employee_id, 4, 7, date, employee_branch))
        self.db.commit()

        self.lineEdit_45.setText("")
        self.lineEdit_48.setText("")
        self.lineEdit_43.setText("")
        self.lineEdit_46.setText("")
        self.lineEdit_44.setText("")
        self.comboBox_22.setCurrentIndex(0)
        self.lineEdit_49.setText("")
        self.groupBox_9.setEnabled(False)

        QMessageBox.information(self, "success", "Employee Edited Successfully")

        self.Show_History()


###################################################
#####

    def Add_Employee_Permission(self):

        employee_name = self.comboBox_19.currentText()

        if self.checkBox_24.isChecked():
            self.cur.execute("""
                        INSERT INTO employee_permissions (employee_name, books_tab, clients_tab, dashboard_tab, history_tab, reports_tab, settings_tab, add_book, edit_book, delete_book, import_books, export_books, add_client, edit_client, delete_client, import_clients, export_clients, add_branch, add_publisher, add_author, add_category, add_employee, edit_employee, is_admin)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """, (
            employee_name, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))

            self.db.commit()
            QMessageBox.information(self, "success", "Permissions Have been Added Successfully")
        else:
            books_tab = 0
            clients_tab = 0
            dashboard_tab = 0
            history_tab = 0
            reports_tab = 0
            settings_tab = 0

            add_book = 0
            edit_book = 0
            delete_book = 0
            import_books = 0
            export_books = 0

            add_client = 0
            edit_client = 0
            delete_client = 0
            import_clients = 0
            export_clients = 0

            add_branch = 0
            add_publisher = 0
            add_author = 0
            add_category = 0
            add_employee = 0
            edit_employee = 0

            if self.checkBox_7.isChecked():
                books_tab = 1
            if self.checkBox_8.isChecked():
                clients_tab = 1
            if self.checkBox_9.isChecked():
                dashboard_tab = 1
            if self.checkBox_10.isChecked():
                history_tab = 1
            if self.checkBox_11.isChecked():
                reports_tab = 1
            if self.checkBox_12.isChecked():
                settings_tab = 1

            if self.checkBox.isChecked():
                add_book = 1
            if self.checkBox_2.isChecked():
                edit_book = 1
            if self.checkBox_3.isChecked():
                delete_book = 1
            if self.checkBox_14.isChecked():
                import_books = 1
            if self.checkBox_13.isChecked():
                export_books = 1

            if self.checkBox_4.isChecked():
                add_client = 1
            if self.checkBox_5.isChecked():
                edit_client = 1
            if self.checkBox_6.isChecked():
                delete_client = 1
            if self.checkBox_15.isChecked():
                import_clients = 1
            if self.checkBox_16.isChecked():
                export_clients = 1

            if self.checkBox_17.isChecked():
                add_branch = 1
            if self.checkBox_18.isChecked():
                add_publisher = 1
            if self.checkBox_19.isChecked():
                add_author = 1
            if self.checkBox_20.isChecked():
                add_category = 1
            if self.checkBox_21.isChecked():
                add_employee = 1
            if self.checkBox_22.isChecked():
                edit_employee = 1

            self.cur.execute("""
            INSERT INTO employee_permissions (employee_name, books_tab, clients_tab, dashboard_tab, history_tab, reports_tab, settings_tab, add_book, edit_book, delete_book, import_books, export_books, add_client, edit_client, delete_client, import_clients, export_clients, add_branch, add_publisher, add_author, add_category, add_employee, edit_employee)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,(employee_name, books_tab, clients_tab, dashboard_tab, history_tab, reports_tab, settings_tab, add_book, edit_book, delete_book, import_books, export_books, add_client, edit_client, delete_client, import_clients, export_clients, add_branch, add_publisher, add_author, add_category, add_employee, edit_employee))

            self.db.commit()
            QMessageBox.information(self, "success", "Permissions Have been Added Successfully")


    def Admin_Report(self):
        pass

##################################################
#####

    def Open_Login_Tab(self):
        self.tabWidget.setCurrentIndex(0)


    def Open_Reset_Password_Tab(self):
        self.tabWidget.setCurrentIndex(1)


    def Open_Daily_Movements_Tab(self):
        self.tabWidget.setCurrentIndex(2)


    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_2.setCurrentIndex(0)


    def Open_Clients_Tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.tabWidget_3.setCurrentIndex(0)


    def Open_Dashboard_Tab(self):
        self.get_dashboard_data()
        self.tabWidget.setCurrentIndex(5)


    def Open_History_Tab(self):
        self.tabWidget.setCurrentIndex(6)


    def Open_Report_Tab(self):
        self.tabWidget.setCurrentIndex(7)
        self.tabWidget_5.setCurrentIndex(0)


    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_4.setCurrentIndex(0)

    def get_dashboard_data(self):

        year = self.dateEdit_7.date()
        year = year.toPyDate()
        year = str(year).split("-")[0]

        self.cur.execute("""
        SELECT COUNT(book_id) , EXTRACT(MONTH FROM book_from) as month FROM dailymovements WHERE year(book_from) = %s GROUP BY month
        """%(year))
        data = self.cur.fetchall()
        pen = pg.mkPen(color=(255,0,0))

        books_count = []
        rent_count = []

        for row in data:
            books_count.append(row[0])
            rent_count.append(row[1])

        barchart = pg.BarGraphItem(x = books_count,height=rent_count,width = .2,pen = pen)
        self.widget.addItem(barchart)
        #self.widget.plot(data1, data2, pen=pen, symbol="+", symbolSize=20, symbolBrush=('w'))

        self.widget.setTitle("Activities")
        self.widget.addLegend()
        self.widget.setLabel("left", "Book Number", color = "red", size =40)
        self.widget.setLabel("bottom", "Month", color = "red", size =40)
        self.widget.showGrid(x=True,y=True)



def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()