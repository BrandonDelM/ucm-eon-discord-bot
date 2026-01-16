import sqlite3

def create_database():
    conn = sqlite3.connect("database.db")

def table_exists(table_name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    item_check = c.fetchone()
    if item_check is not None:
        return True
    return False


def create_table(table_name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(f"""
        CREATE TABLE "{table_name}" (
            poster text,
            title text,
            start_time text,
            end_time text,
            building text,
            link text
        )
    """)
    conn.commit()
    conn.close()

def add_many_to_table(list, table_name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.executemany(f'INSERT INTO "{table_name}" VALUES (?,?,?,?,?,?)', (list))

    conn.commit()
    conn.close()

def add_to_table(table_name, poster="",title="",start_time="",end_time="",building="",link=""):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(f'INSERT INTO "{table_name}" VALUES (?,?,?,?,?,?)', (poster,title,start_time,end_time,building,link))

    conn.commit()
    conn.close()

def clear_table(table_name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(f"DELETE FROM {table_name}")
    conn.commit()
    conn.close()

def delete_from_table(table_name,id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    id = str(id)

    c.execute(f'DELETE FROM "{table_name}" WHERE rowid = (?)', (id,))
    conn.commit()
    conn.close()

def get_all_rows_from_table(table_name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(f'SELECT * FROM "{table_name}"')
    items = c.fetchall()

    conn.commit()
    conn.close()

    return items