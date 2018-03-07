import MySQLdb
from config import *
def db_query(query):
	print query
	res = []
	db_con = MySQLdb.connect(db_host, db_user, db_passwd, db)
	cur = db_con.cursor()
	if cur:
		cur.execute(query)
		db_con.commit()
		print "saved to DB"
		res = cur.fetchall()
		cur.close()
	db_con.close()
	return res
