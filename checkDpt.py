# importing required libraries
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
 
dataBase = mysql.connector.connect(
  host=os.getenv("DB_HOST"),              
  user=os.getenv("DB_USER"),
  passwd=os.getenv("DB_PASSWORD")
)

print(dataBase)

print("Enter a departament id to view their products")

# cursor object
cursorObject = dataBase.cursor()
 
# Querry
query = "SELECT NAME, ROLL FROM STUDENT"
cursorObject.execute(query)

# Disconnecting from the server
dataBase.close()
