import psycopg2

hostname = 'balarama.db.elephantsql.com'
username = 'nmnwuopl' # the username when you create the database
password = 'O6eGuGRaw1iqOeU4xecihU0kESQkRhUo' #change to your password
database = 'nmnwuopl'

def queryQuotes( conn ) :
    cur = conn.cursor()
    cur.execute( """select * from amako""" )
    rows = cur.fetchall()
    for row in rows :
        print (row[5])

conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
queryQuotes( conn )
conn.close()