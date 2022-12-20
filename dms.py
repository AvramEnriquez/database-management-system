import psycopg2
 
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = ""
DB_HOST = "localhost"
DB_PORT = "5432"

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
    CREATE TABLE employee
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
INSERT INTO employee (name, email)
VALUES ('{name}', '{email}');
""")

# Commit the changes
conn.commit()
print("Employee inputted successfully")