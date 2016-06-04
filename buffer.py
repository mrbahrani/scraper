import sqlite3

def searchInDB(keyword):
    result = []
    conn = sqlite3.connect('database.db')
    query = "SELECT * from APPS WHERE NAME LIKE "
    query = query + "'%" + keyword + "%'"
    query += "or PAKAGE LIKE" + "'%" + keyword + "%'"
    cursor = conn.execute(query)
    for row in cursor:
        dic = {'name': row[1], 'price': row[2], 'pakage': row[3] , 'category': row[4]}
        result.append(dic)
    print result
