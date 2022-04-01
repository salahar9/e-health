import pymysql

db_name = 'sql11481732'
connection = pymysql.connect(host="sql11.freesqldatabase.com", user="sql11481732", passwd="IxcCRn59jy", database=db_name)
cursor = connection.cursor()

# cursor.execute(f'''
#     SELECT *
#     FROM {db_name}.users
# ''')
#
# print(cursor.fetchone())

