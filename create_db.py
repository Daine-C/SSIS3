import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    )

my_curr = mydb.cursor()

#my_curr.execute("CREATE DATABASE SSIS")

my_curr.execute("SHOW DATABASES")
for db in my_curr:
    print(db)