import mysql.connector
import os
from mysql.connector import Error 
from dotenv import load_dotenv

load_dotenv()

try:
  dataBase = mysql.connector.connect(
    host=os.getenv("DB_HOST"),              
    user=os.getenv("DB_USER"),
    passwd=os.getenv("DB_PASSWORD"),
    database="Uppsala"  
  )

  if dataBase.is_connected():
    print(f"Connected to MySQL Server version {dataBase.get_server_info()}")
    cursor = dataBase.cursor()

    print("Enter a departament id to view their products")

    try:
        dept_id = int(input("\nEnter a departament id to view their products: "))
    except ValueError:
        print("Please enter a number.")
        quit()

    query_children = "SELECT department_id, title FROM Department WHERE parent_id = %s"
    cursor.execute(query_children, (dept_id,))
    children = cursor.fetchall()
      
    if children:
      print(f"\nDepartment {dept_id} is a Parent Department.")
      print("----------------")
      print(f"{'ID':<10} | {'Sub-Department Title'}")
      print("----------------")
      
      for child in children:
          print(f"{child[0]:<10} | {child[1]}")

    else:
      print(f"\nDepartment {dept_id} is a Leaf Department. Listing products...")
                
      query_products = """
          SELECT 
              product_id, 
              title, 
              current_price * (1 - discount_percentage / 100.0) as final_price
          FROM Product 
          WHERE department_id = %s
      """
      cursor.execute(query_products, (dept_id,))
      products = cursor.fetchall()

      if products:
          print("----------------")
          print(f"{'ID':<5} | {'Title':<35} | {'Price (Discounted)'}")
          print("----------------")
          
          for prod in products:
              p_id = prod[0]
              title = prod[1]
              price = f"${prod[2]:.2f}" 
              
              print(f"{p_id:<5} | {title:<35} | {price}")
      else:
          print(f"No products found in Department {dept_id} (or Department does not exist).")

except Error as e:
    print(f"SQL ERROR: {e}")
 
finally:
    if 'dataBase' in locals() and dataBase.is_connected():
        if 'cursor' in locals():
            cursor.close()
        dataBase.close()
        print("\nMySQL connection is closed")