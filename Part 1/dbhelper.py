import sqlite3
from datetime import datetime
from datetime import timedelta

DB_PATH = './test.db'   # Update this path accordingly

def addTodo(task, status, date):
    try:
        conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        date = datetime.strptime(date, "%Y-%m-%d")

        # Once a connection has been established, we use the cursor
        # object to execute queries
        c = conn.cursor()

        # Keep the initial status as Not Started
        c.execute('insert into todos (task, status, due_by) values(?,?,?)', (task, status, date))

        # We commit to save the change
        conn.commit()
        return True
    except Exception as e:
        print('Error: ', e)
        return False

def fetchAll():
    try:
        conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cursor = conn.execute("SELECT * FROM TODOS")
        result = []
        for row in cursor:
            result.append({'id' : row[0], 'task': row[1], 'due_by' : row[3], 'status':row[2]})
        return result
    except Exception as e:
        print('Error: ', e)
        return

def fetchById(id):
    try:
        conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cursor = conn.execute("SELECT * FROM TODOS WHERE ID="+str(id))
        for row in cursor:
            return {'id' : row[0], 'task': row[1], 'due_by' : row[3], 'status':row[2]}
    except Exception as e:
        print('Error: ', e)
        return

def fetchDue(date):
    try:
        conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        currentDay = datetime.strptime(date, "%Y-%m-%d")
        currentDay = currentDay.strftime("%Y-%m-%d %H:%M:%S.%f")
        print(f"SELECT * FROM TODOS WHERE DUE_BY = '{currentDay}'")
        cursor = conn.execute(f"SELECT * FROM TODOS WHERE DUE_BY > '{currentDay}' AND DUE_BY < '{nextDay}'")
        result = []
        for row in cursor:
            result.append({'id' : row[0], 'task': row[1], 'due_by' : row[3], 'status':row[2]})
        return result
    except Exception as e:
        print('Error: ', e)
        return []


def fetchOverDue():
    try:
        conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        cursor = conn.execute(f"SELECT * FROM TODOS WHERE DUE_BY > '{now}' AND STATUS!='FINISHED'")
        result = []
        for row in cursor:
            result.append({'id' : row[0], 'task': row[1], 'due_by' : row[3], 'status':row[2]})
        return result
    except Exception as e:
        print('Error: ', e)
        return []

def deleteById(id):
    try:
        conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        conn.execute(f"DELETE FROM TODOS WHERE ID={id}")
        return True
    except Exception as e:
        print('Error: ', e)
        return False

def updateTaskById(task, status, date, id):
    try:
        conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")

        c = conn.cursor()
        c.execute('UPDATE TODOS SET task = ?, status = ?, due_by = ? WHERE id = ?', (task, status, date, id))
        conn.commit()
        return True
    except Exception as e:
        print('Error: ', e)
        return False