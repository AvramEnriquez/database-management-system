import psycopg2
 
# Insert database name, username, password, server address, and port here.
# Leave blank if empty
DB_NAME = ""
DB_USER = ""
DB_PASS = ""
DB_HOST = ""
DB_PORT = ""

try:
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    print("Database connected successfully")
except:
    print("Database not connected successfully")

try:
    cur = conn.cursor()  # Create a cursor
 
    # Execute query to create table
    cur.execute("""
    CREATE TABLE profile
    (
        id SERIAL PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)
    print("Table Created successfully")
except psycopg2.errors.DuplicateTable:
    # If table already exists, state it
    print("Table already exists.")

conn.commit()  # Commit the change regardless

name = input('Input Name:')
email = input('Input Email:')

cur = conn.cursor()  # Creating cursor

cur.execute(f"""
INSERT INTO profile (name, email)
VALUES ('{name}', '{email}');
""")

conn.commit()  # Commit the changes
print("Profile inputted successfully")