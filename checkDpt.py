# importing required libraries
import mysql.connector
 
dataBase = mysql.connector.connect(
  host ="localhost",                # Localhost for local connection
  user ="user",
  passwd ="password"
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
