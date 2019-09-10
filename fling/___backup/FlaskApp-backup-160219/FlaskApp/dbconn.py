import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
			user = "root",
			passwd = "",
			db = "fling_test")

    c = conn.cursor()

    return c, conn
