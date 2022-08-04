# importujemy moduł sqlite
import sqlite3
from sqlite3 import Error

# Tworzymy połączenie
def create_connection(db_file):
    """create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
        return conn
    except Error as e:
        print(e)
    return conn


# Tworzenie tabeli sql - w naszym przypadku create_projects_sql
def execute_sql(conn, create_projects_sql):
    """Execute create_projects_sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    # conn = sqlite3.connect(db_file)

    try:
        c = conn.cursor()
        c.execute(create_projects_sql)
        print("Kod wykonany")
    except Error as e:
        print(e)

# Tworzenie kolejnej tabeli sql - w naszym przypadku create_tasks_sql
def execute_sql(conn, create_tasks_sql):
    """Execute create_tasks_sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    # conn = sqlite3.connect(db_file)

    try:
        c = conn.cursor()
        c.execute(create_tasks_sql)
        print("Kod wykonany")
    except Error as e:
        print(e)


create_projects_sql = """
-- projects tables
CREATE TABLE IF NOT EXISTS projects (
    id integer PRIMARY KEY,
    nazwa text NOT NULL,
    start_date text,
    end_date text
);
"""

create_tasks_sql = """
-- zadanie table
CREATE TABLE IF NOT EXISTS tasks (
    id integer PRIMARY KEY,
    projekt_id integer NOT NULL,
    nazwa VARCHAR(250) NOT NULL,
    opis TEXT,
    status VARCHAR(15) NOT NULL,
    start_date text NOT NULL,
    end_date text NOT NULL,
    FOREIGN KEY (projekt_id) REFERENCES projects (id)
);
"""

# Dodawanie nowych pozycji do projektu
def add_project(conn, projects: tuple):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    create_projects_sql  = """INSERT INTO projects(nazwa, start_date, end_date)
             VALUES("Forma na wakacje 2023 bo na te się nie udało", "01.01.2023", "01.05.2023")"""
    cur = conn.cursor()
    cur.execute(create_projects_sql , projects)
    cur.commit(create_projects_sql , projects)
    print("Utworzono")
    return cur.lastrowid


# Dodawanie nowych pozycji do listy zadań
def add_task(conn, tasks: tuple):
    """
    Create a new task into the tasks table
    :param conn:
    :param task:
    :return: task id
    """
    create_tasks_sql = """INSERT INTO tasks(project_id, nazwa, opis, status, start_date, end_date)
             VALUES("Siłownia", "Zapisać się na siłownię", "Done", "01.01.2023", "01.05.2023")"""
    cur = conn.cursor()
    cur.execute(create_tasks_sql, tasks)
    conn.commit()
    return cur.lastrowid


# Korzystamy z jednej z dostępnych metod do pobierania danych z kursora: fetchall(all czyli pobieramy wszystkie dane np. z tabeli "tasks")
def select_all(conn, tasks):
    """
    Query all rows in the table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {tasks}")
    rows = cur.fetchall()

    return rows


# Podobnie jak wyzej, za pomocą metody fetchall pobieramy dane filtrując np. po statusie w tabeli tasks
def select_task_by_status(conn, status):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param status:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE status=?", (status,))

    rows = cur.fetchall()
    return rows


# za pomocą metody fetchall pobieramy dane filtrując konkretną tabelę (np. tasks), argumenty oraz wartości)
def select_where(conn, tasks, **query):
    """
    Query tasks from tasks with data from **query dict
    :param conn: the Connection object
    :param tasks: tasks name
    :param query: dict of attributes and values
    :return:
    """
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    cur.execute(f"SELECT * FROM {tasks} WHERE {q}", values)
    rows = cur.fetchall()
    return rows


# aktualizacja danych w tabelach, (table mozemy zastąpić nazwą tabeli np tasks)
def update(conn, table, id, **kwargs):
    """
    update status, begin_date, and end date of a task
    :param conn:
    :param table: table name
    :param id: row id
    :return:
    """
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id,)

    sql = f""" UPDATE {table}
             SET {parameters}
             WHERE id = ?"""
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("OK")
    except sqlite3.OperationalError as e:
        print(e)


# usuwanie konkretnego zadania (delete_where) oraz całej tabeli (delete_all)
def delete_where(conn, table, **kwargs):
    """
    Delete from table where attributes from
    :param conn:  Connection to the SQLite database
    :param table: table name
    :param kwargs: dict of attributes and values
    :return:
    """
    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)

    sql = f"DELETE FROM {table} WHERE {q}"
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Deleted")


def delete_all(conn, table):
    """
    Delete all rows from table
    :param conn: Connection to the SQLite database
    :param table: table name
    :return:
    """
    sql = f"DELETE FROM {table}"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Deleted")



if __name__ == "__main__":
    db_file = "database.db"
    conn = create_connection("database.db")
    

    projects = (
        "Forma na wakacje 2023 bo na te się nie udało",
        "01.01.2023",
        "01.05.2023",
    )
    
    pr_id = add_project(conn, projects)

    tasks = (
        pr_id,
        "Siłownia",
        "Zapisać się na siłownię",
        "Done",
        "01.01.2023",
        "01.05.2023",
    )

    task_id = add_task(conn, tasks)

    print(pr_id, task_id)
    conn.commit()

conn = create_connection(r"database.db")
# execute_sql(conn, create_tasks_sql)

p = add_project(conn, projects)
print(p)
conn.commit()

projects = select_all(conn, "projects")
print(projects)
conn.close()
# print(help(create_connection))
