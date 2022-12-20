"""Create and manage a database"""
import psycopg2

valid_database = False

while valid_database == False:
    # Insert database name, username, password, server address, and port here.
    # Leave blank if empty
    DB_NAME = input("Insert database name: ")
    DB_USER = input("Insert database username: ")
    DB_PASS = input("Insert database password (leave blank if empty): ")
    DB_HOST = input("Insert database hostname/server address: ")
    DB_PORT = input("Insert database port: ")

    DB_NAME1 = 'postgres'
    DB_USER1 = 'postgres'
    DB_PASS1 = ''
    DB_HOST1 = 'localhost'
    DB_PORT1 = '5432'

    try:
        postdb = psycopg2.connect(
            database=DB_NAME1,
            user=DB_USER1,
            password=DB_PASS1,
            host=DB_HOST1,
            port=DB_PORT1)
        print("Database connected successfully!")
        valid_database = True
    except:
        print("Database failed to connect.")

def create_table():
    table_name = input("Create Table name: ")

    try:
        cur = postdb.cursor()  # Create a cursor
    
        # Execute query to create table
        cur.execute(f"""
            CREATE TABLE {table_name} 
            (id SERIAL PRIMARY KEY NOT NULL)
        ;""")
        print(f"{table_name} Table created successfully with serial ID column.")
    except psycopg2.errors.DuplicateTable:
        # State if table already exists
        print(f"{table_name} Table already exists.")

    postdb.commit()  # Commit the change regardless

def add_column():
    table = input("Which table? ")
    column_name = input("Add column name: ")
    datatype = input("Add column data type: ")

    try:
        cur = postdb.cursor()  # Create a cursor
    
        # Execute query to alter table
        cur.execute(f"""
            ALTER TABLE {table} 
            ADD {column_name} {datatype}
        ;""")
        print(f"Column '{column_name}' datatype '{datatype}' added successfully!")
    except psycopg2.errors.DuplicateColumn:
        # State if column already exists
        print(f"Column '{column_name}' already exists.")
    except:
        # State if other errors occur, syntax, etc.
        print(f"Invalid data type, please try again.")

    postdb.commit()  # Commit the change regardless

def add_user():
    table = input("Table name: ")

    cur = postdb.cursor()  # Creating cursor

    cur.execute(f"""
        SELECT *
        FROM {table}
    ;""")

    col = []
    column_names = [desc[0] for desc in cur.description]
    s = '(' + ', '.join(column_names[1:]) + ')'
    print(s)

    for column in column_names[1:]:
        col.append(input(f"Input {column}: "))
    
    col1 = tuple(col)
    cur.execute(f"""
        INSERT INTO {table} {s}
        VALUES {col1}
    ;""")

    postdb.commit()  # Commit the changes

def done():
    print("Done!")

function_dict = {'create_table':create_table, 'add_column':add_column, 'add_user':add_user, 'done':done}
command = ''

while command != 'done':
    command = input("What would you like to do? Type done if you are finished: ")
    function_dict[command]()
