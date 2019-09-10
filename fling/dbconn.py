import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
			user = "root",
			passwd = "",
			db = "flingair")

    cursor = conn.cursor()

    return cursor, conn
