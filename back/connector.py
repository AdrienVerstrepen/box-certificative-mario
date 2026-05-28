import psycopg2

# Connect to the School database
conn = psycopg2.connect(
    dbname="box-certificative-mario",
    user="postgres",
    password="Mathys59.",
    host="localhost"
)

email = "alice@mail.com"
mdp = "pass123"

cursor = conn.cursor()
cursor.execute("SELECT UserPassword FROM AppUser WHERE email like %s;", (email,))
result = cursor.fetchone()
print(result)
if result is not None:
    stored_password = result[0]
    if stored_password == mdp:
        print("Authentication successful!")
    else:
        print("Authentication failed: Incorrect password.")

cursor.close()
conn.close()