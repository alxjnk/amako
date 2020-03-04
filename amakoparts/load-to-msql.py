

import sys
import pymysql


def csv_to_mysql(load_sql, host, user, password):
    '''
    This function load a csv file to MySQL table according to
    the load_sql statement.
    '''
    try:
        con = pymysql.connect(host=host,
                              user=user,
                              password=password,
                              autocommit=True,
                              local_infile=1)
        print('Connected to DB: {}'.format(host))
        # Create cursor and execute Load SQL
        cursor = con.cursor()
        cursor.execute(load_sql)
        print('Succuessfully loaded the table from csv.')
        con.close()

    except Exception as e:
        print('Error: {}'.format(str(e)))
        sys.exit(1)


load_product = (""" LOAD DATA LOCAL INFILE 'output.csv' INTO TABLE oc_product
FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES
(@dummy, @dummy, @dummy, oc_product.manufacturer, @dummy, oc_product.price.model, oc_product.price, oc_product.quantity)
""")
# load_manufacturer = "LOAD DATA LOCAL INFILE '/output.csv' INTO TABLE oc_product\
# FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES(col1, col2, col3, col4, col5...)
# "
# load_product_description = "LOAD DATA LOCAL INFILE '/output.csv' INTO TABLE oc_product\
# FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES(col1, col2, col3, col4, col5...)
# "
host = 'base.bs-studio.gq/'
user = 'bsstudiogq_test'
password = 'sAh5Gs^YB%TM1'
csv_to_mysql(load_product, host, user, password)
# csv_to_mysql(load_manufacturer, host, user, password)
# csv_to_mysql(load_product_description, host, user, password)
