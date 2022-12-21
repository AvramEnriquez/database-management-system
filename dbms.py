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

    try:
        postdb = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT)
        print("Database connected successfully!")
        valid_database = True
    except:
        print("Database failed to connect.")

def create_table():
    table_name = input("Create Table name: ")

    try:
        # Create a cursor
        cur = postdb.cursor()
    
        # Execute query to create table
        cur.execute(f"""
            CREATE TABLE {table_name} 
            (id SERIAL PRIMARY KEY NOT NULL)
            ;""")
        print(f"{table_name} Table created successfully with serial ID column.")

    except psycopg2.errors.DuplicateTable:
        # State if table already exists
        print(f"{table_name} Table already exists.")

    postdb.commit()  # Commit the change
    cur.close()  # Close cursor

def add_column():
    table = input("Which table? ")
    column_name = input("Add column name: ")
    datatype = input("Add column data type: ")

    try:
        # Create a cursor
        cur = postdb.cursor()

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
        print(f"Something went wrong, please try again.")

    postdb.commit()  # Commit the change
    cur.close()  # Close cursor

def add_user():
    table = input("Table name: ")

    # Create a cursor
    cur = postdb.cursor()

    cur.execute(f"""
        SELECT *
        FROM {table}
        ;""")

    values = []
    # Pull column names into list
    col_name_list = [desc[0] for desc in cur.description]

    # Remove quotation marks from list and wrap in ()
    # Ignore ID column name since ID auto-increments
    column_names = '(' + ', '.join(col_name_list[1:]) + ')'
    print(column_names)

    for variable in col_name_list[1:]:
        values.append(input(f"Input {variable}: "))

    cur.execute(f"""
        INSERT INTO {table} {column_names}
        VALUES {tuple(values)}
        ;""")

    postdb.commit()  # Commit the changes
    cur.close()  # Close cursor

def done():
    postdb.close()
    print("Done!")

function_dict = {'create_table':create_table, 'add_column':add_column, 'add_user':add_user, 'done':done}
command = ''

while command != 'done':
    print("")
    command = input("What would you like to do?\n"
        "'create_table' creates a new table,\n"
        "'add_column' adds a new column to an existing table,\n"
        "'add_user' adds a new entity to an existing table,\n"
        "Type 'done' when you are finished: ")
    function_dict[command]()
