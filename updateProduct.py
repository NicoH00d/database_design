import mysql.connector
import os
from mysql.connector import Error 
from dotenv import load_dotenv

load_dotenv()

try:
    # Connect to database
    dataBase = mysql.connector.connect(
        host=os.getenv("DB_HOST"),              
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASSWORD"),
        database="Uppsala"  # Essential: Select the database to use
    )

    if dataBase.is_connected():
        print(f"Connected to MySQL Server version {dataBase.get_server_info()}")
        cursor = dataBase.cursor()

        print("Update Product Discount")
        
        # Ask for Product ID
        try:
            prod_id = int(input("\nEnter the Product ID: "))
        except ValueError:
            print("Please enter a valid number.")
            quit()

        #  Check if product exists and get current discount
        query_check = "SELECT title, discount_percentage FROM Product WHERE product_id = %s"
        cursor.execute(query_check, (prod_id,))
        product = cursor.fetchone()

        if product:
            current_title = product[0]
            current_discount = product[1]

            print(f"\nProduct Found: {current_title}")
            print(f"Current Discount: {current_discount}%")
            
            # Ask for new discount
            try:
                new_discount = int(input("Enter new discount percentage (0-100): "))
                
                # Basic validation
                if new_discount < 0 or new_discount > 100:
                    print("Error: Discount must be between 0 and 100.")
                    quit()
                    
            except ValueError:
                print("Invalid input. Cancelling update.")
                quit()

            # Perform the Update
            query_update = "UPDATE Product SET discount_percentage = %s WHERE product_id = %s"
            cursor.execute(query_update, (new_discount, prod_id))
            
            # Commit the transaction to save changes
            dataBase.commit()
            
            print(f"Success! Discount for '{current_title}' updated to {new_discount}%.")

        else:
            print(f"Product with ID {prod_id} not found.")

except Error as e:
    print(f"SQL ERROR: {e}")

finally:
    # Clean up
    if 'dataBase' in locals() and dataBase.is_connected():
        cursor.close()
        dataBase.close()
        print("\nMySQL connection is closed")