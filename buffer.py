import sqlite3
import staff

def searchInDB(keyword):
    result = []
    conn = sqlite3.connect('database.db')
    query = "SELECT * from APPS WHERE NAME LIKE "
    query = query + "'%" + keyword + "%'"
    query += "or PAKAGE LIKE" + "'%" + keyword + "%'"
    cursor = conn.execute(query)
    for row in cursor:
        dic = {'name': row[1], 'price': row[2], 'icon': staff.getIcon(row[3]) , 'url': staff.getUrl(row[3]), 'category': row[4]}
        result.append(dic)
    return result

print searchInDB("foot")
