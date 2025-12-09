
import pymysql
import getpass
from sshtunnel import SSHTunnel

group_name = "ht25_2_1dl301_group_7"
group_password = "pasSWd_7"

def check_department(mydb):
	mycursor = mydb.cursor()
	
	print("Enter a departament id to view their products")

	try:
		dept_id = int(input("\nEnter a departament id to view their products: "))
	except ValueError:
		print("Please enter a number.")
		mycursor.close()
		return

	query_children = "SELECT department_id, title FROM Department WHERE parent_id = %s"
	mycursor.execute(query_children, (dept_id,))
	children = mycursor.fetchall()
	
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
		mycursor.execute(query_products, (dept_id,))
		products = mycursor.fetchall()

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

	mycursor.close()

def update_product(mydb):
	mycursor = mydb.cursor()
	
	print("Update Product Discount")
	
	# Ask for Product ID
	try:
		prod_id = int(input("\nEnter the Product ID: "))
	except ValueError:
		print("Please enter a valid number.")
		mycursor.close()
		return

	# Check if product exists and get current discount
	query_check = "SELECT title, discount_percentage FROM Product WHERE product_id = %s"
	mycursor.execute(query_check, (prod_id,))
	product = mycursor.fetchone()

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
				mycursor.close()
				return
				
		except ValueError:
			print("Invalid input. Cancelling update.")
			mycursor.close()
			return

		# Perform the Update
		query_update = "UPDATE Product SET discount_percentage = %s WHERE product_id = %s"
		mycursor.execute(query_update, (new_discount, prod_id))
		
		# Commit the transaction to save changes
		mydb.commit()
		
		print(f"Success! Discount for '{current_title}' updated to {new_discount}%.")

	else:
		print(f"Product with ID {prod_id} not found.")

	mycursor.close()

def program(mydb):
	print("\n=== Database Menu ===")
	print("1. Check Department")
	print("2. Update Product Discount")
	
	try:
		choice = int(input("\nSelect an option (1-2): "))
	except ValueError:
		print("Invalid input.")
		return
	
	if choice == 1:
		check_department(mydb)
	elif choice == 2:
		update_product(mydb)
	else:
		print("Invalid option.")

def db_connect(host, port):
	mydb = pymysql.connect(
		database=group_name,
		user=group_name,
		password=group_password, 
		host=host, 
		port=port
	)

	program(mydb)

	mydb.close()
	
if __name__ == '__main__':
	ssh_username = input("Enter your Studium username: ")
	ssh_password = getpass.getpass("Enter your Studium password A: ")

	tunnel = SSHTunnel(ssh_username, ssh_password, 'fries.it.uu.se', 22)
	tunnel.start(local_host='127.0.0.1', local_port=3306, remote_host='127.0.0.1', remote_port=3306)

	# Now the tunnel is ready, connect to DB
	db_connect(tunnel.local_host, tunnel.local_port)

	# Stop the tunnel
	tunnel.stop()
