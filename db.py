import pymysql
import csv
con = pymysql.connect('127.0.0.1', 'agronova_as',
    '_ccZ9a(f$wpB', 'agronova_bs')

try:
    with con.cursor() as cursor:
        # Create a new record
        # sql = "SELECT * FROM oc_product"
        sql = "INSERT INTO oc_product (image, manufacturer_id, price, quantity, product_id) VALUES"
        with open('./amakoparts/output.csv') as csvfile:
            spamreader = csv.DictReader(csvfile)
            for row in spamreader:
                sql = sql + "(%s,%s,%s,%s,%s)".format(row['image'], row['manufacturer'], row['price'], row['quantity'], row['title'])
        print(sql)
        # sql = """LOAD DATA INFILE
        #         '/home/agronova/parse/amako/amakoparts/output.csv'
        #         INTO TABLE oc_product
        #         FIELDS TERMINATED BY ','
        #         ENCLOSED BY '"'
        #         LINES TERMINATED BY '\n'
        #         IGNORE 1 ROWS
        #         (@dummy,@dummy, @dummy, image, manufacturer_id, @dummy, @dummy, price, quantity, @dummy, @dummy, product_id);"""
        # csv_data = csv.reader(file('./amakoparts/output.csv'))
        # for row in csv_data:
        #     print(row)
        # with open('./amakoparts/output.csv', newline='') as csvfile:
        #     spamreader = csv.reader(csvfile, delimiter=',')
        #     for row in spamreader:
        #         if row[0] == 'DT_RowId':
        #             pass
        #         else:
        #             print(row) 

        # cursor.execute('INSERT INTO testcsv(names, \
        #   classes, mark )' \
        #   'VALUES("%s", "%s", "%s")',
        #   row)
        # cursor.execute(sql)
        # result = cursor.fetchone()
        # print(result)

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

