import mysql.connector
import os
user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')
host = os.getenv('host')
port = os.getenv('port')


def select(q):
	con = mysql.connector.connect(user=user, password=password, host=host, database=database, port=port)
	cur=con.cursor(dictionary=True)
	cur.execute(q)
	result=cur.fetchall()
	cur.close()
	con.close()
	return result

def insert(q):
	con = mysql.connector.connect(user=user, password=password, host=host, database=database, port=port)
	cur=con.cursor(dictionary=True)
	cur.execute(q)
	con.commit()
	result=cur.lastrowid
	cur.close()
	con.close()
	return result

def update(q):
	con = mysql.connector.connect(user=user, password=password, host=host, database=database, port=port)
	cur=con.cursor(dictionary=True)
	cur.execute(q)
	con.commit()
	res=cur.rowcount
	cur.close()
	con.close()
	return res

def delete(q):
	con = mysql.connector.connect(user=user, password=password, host=host, database=database, port=port)
	cur=con.cursor(dictionary=True)
	cur.execute(q)
	con.commit()
	result=cur.rowcount
	cur.close()
	con.close()
	return result