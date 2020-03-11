import pymysql
 
con = pymysql.connect('127.0.0.1', 'agronova_as', 
    '_ccZ9a(f$wpB', 'agronova_bs')
 
try:
    with con.cursor() as cursor:
        # Create a new record
        # sql = "SELECT * FROM oc_product"
        sql = """LOAD DATA INFILE 
                '/home/agronova/parse/amako/amakoparts/output.csv'
                INTO TABLE oc_product  
                FIELDS TERMINATED BY ',' 
                ENCLOSED BY '"'
                LINES TERMINATED BY '\n'
                IGNORE 1 ROWS
                (@dummy,@dummy, @dummy, image, manufacturer_id, @dummy, @dummy, price, quantity, @dummy, @dummy, product_id);"""
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    # con.commit()

    # with con.cursor() as cursor:
    #     # Read a single record
    #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
    #     cursor.execute(sql, ('webmaster@python.org',))
    #     result = cursor.fetchone()
    #     print(result)
finally:
    con.close()