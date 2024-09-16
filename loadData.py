import hashlib
import mysql.connector
import sql_tools as sqltool

file1 = "credentials_short.txt"

# Connect to MySQL database
con = sqltool.connect()
cursor = con.cursor()
skipped = 0
# Open and process the credentials file
with open(file1, 'r', encoding='utf-8') as file:
  for line in file:

    # Break up lines by colon
    parts = line.split(':')

    if len(parts) != 2:
      print(f"Skipping invalid line: {line} ")
      skipped += 1
      continue

    # Hash email and password
    user = hashlib.sha256(parts[0].encode('utf-8'), usedforsecurity=True).hexdigest()
    password = hashlib.sha256(parts[1].strip().encode('utf-8'), usedforsecurity=True).hexdigest()

    # Prepare SQL query to insert hashed values into the database
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    values = (user, password)
    try:
      cursor.execute(sql, values)
    # Duplicates
    except mysql.connector.IntegrityError as e:
      skipped += 1
      print(f"Duplicate Email {parts[0]} : {e}")

con.commit()
print (f"Finished! Skipped {skipped} duplicate users")
# Close the cursor and connection
cursor.close()
con.close()
