import pymysql
 
con = pymysql.connect('localhost', 'agronova_parse', 
    '3c91250b!!!', 'agronova_bs')
 
with con:
    
    cur = con.cursor()
    cur.execute("SELECT VERSION()")
 
    version = cur.fetchone()
    
    print("Database version: {}".format(version[0]))