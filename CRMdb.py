
import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Password1234'
    
)

# cursor object
cursorObject = database.cursor()

# create database
cursorObject.execute("CREATE DATABASE CRM_db")

print("Done.")