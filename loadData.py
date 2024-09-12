import hashlib
import mysql.connector

file1 = "credentials_short.txt"

# Connect to MySQL database
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="",
  database="users"
)
cursor = mydb.cursor()

# Open and process the credentials file
with open(file1, 'r', encoding='utf-8') as file:
  for line in file:
    try:
      parts = line.split(':')
      if len(parts) != 2:
        print(f"Skipping invalid line: {line}")
        continue

      # Hash email and password
      user = hashlib.sha256(parts[0].encode('utf-8'), usedforsecurity=True).hexdigest()
      password = hashlib.sha256(parts[1].strip().encode('utf-8'), usedforsecurity=True).hexdigest()
      # Prepare SQL query to insert hashed values into the database
      sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
      values = (user, password)
      cursor.execute(sql, values)

    except ValueError:
      print(f"VALUE ERROR: {line}")
    except Exception as e:
      print(f"ERROR: {e}")

# Commit the changes to the database
mydb.commit()

# Close the cursor and connection
cursor.close()
mydb.close()
